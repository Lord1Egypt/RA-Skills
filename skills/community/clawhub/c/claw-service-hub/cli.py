"""
Claw Service Hub CLI
Command-line interface for managing services via WebSocket
"""

import asyncio
import json
import sys
import uuid
from typing import Optional

import aiohttp
import click
import websockets

# Add project root to path for imports
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Server configuration
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8765
DEFAULT_HTTP_PORT = 5265

# Add a timeout for WebSocket operations
WS_TIMEOUT = 10


def get_http_url(host: str = DEFAULT_HOST) -> str:
    """Get REST API URL"""
    return f"http://{host}:{DEFAULT_HTTP_PORT}"


async def call_api(endpoint: str, method: str = "GET", data: Optional[dict] = None):
    """Make HTTP request to server REST API"""
    url = f"{get_http_url()}{endpoint}"
    async with aiohttp.ClientSession() as session:
        try:
            if method == "GET":
                async with session.get(url) as resp:
                    return await resp.json()
            elif method == "POST":
                async with session.post(url, json=data) as resp:
                    return await resp.json()
            elif method == "DELETE":
                async with session.delete(url) as resp:
                    return await resp.json()
        except aiohttp.ClientError as e:
            click.echo(f"Error connecting to server: {e}", err=True)
            return None


async def ws_send_and_wait(host: str, message: dict) -> Optional[dict]:
    """Send message via WebSocket and wait for response"""
    ws_url = f"ws://{host}:{DEFAULT_PORT}"
    try:
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps(message))
            
            # Wait for response with timeout
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=WS_TIMEOUT)
                return json.loads(response)
            except asyncio.TimeoutError:
                click.echo("Timeout waiting for response", err=True)
                return None
    except Exception as e:
        click.echo(f"WebSocket error: {e}", err=True)
        return None


@click.group()
@click.version_option(version="0.1.0", prog_name="claw-hub")
def cli():
    """Claw Service Hub - Service Marketplace for OpenClaw Subagents"""
    pass


@cli.command()
@click.option("--host", default=DEFAULT_HOST, help="Server host")
@click.option("--port", default=DEFAULT_PORT, help="WebSocket port")
@click.option("--http-port", default=DEFAULT_HTTP_PORT, help="REST API port")
def start(host: str, port: int, http_port: int):
    """Start the Claw Service Hub server"""
    click.echo(f"Starting Claw Service Hub...")
    click.echo(f"  WebSocket: ws://{host}:{port}")
    click.echo(f"  REST API:  http://{host}:{http_port}")
    click.echo(f"  Health:    http://{host}:{http_port}/health")
    
    # Import and run the server
    import sys
    import os
    
    # Ensure project root is in path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Set port environment variables
    os.environ.setdefault("HUB_PORT", str(port))
    os.environ.setdefault("HUB_HTTP_PORT", str(http_port))
    
    try:
        from server.main import HubServer
        
        async def run_server():
            server = HubServer(host=host, port=port)
            await server.start()
        
        asyncio.run(run_server())
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")
    except Exception as e:
        click.echo(f"Error starting server: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
@click.option("--description", "-d", default="", help="Service description")
@click.option("--version", "-v", default="1.0.0", help="Service version")
@click.option("--tags", "-t", multiple=True, help="Service tags")
@click.option("--url", "-u", default="", help="Service endpoint URL")
@click.option("--price", "-p", type=float, default=None, help="Service price")
@click.option("--price-unit", default="次", help="Price unit (e.g., 次, 月, 年)")
@click.option("--host", default=DEFAULT_HOST, help="Server host")
def register(name: str, description: str, version: str, tags: tuple, url: str, price: float, price_unit: str, host: str):
    """Register a new service"""
    click.echo(f"Registering service: {name}")
    
    client_id = f"cli-{uuid.uuid4().hex[:8]}"
    
    # Build service data
    service_data = {
        "name": name,
        "description": description,
        "version": version,
        "tags": list(tags),
    }
    
    # Add endpoint URL if provided
    if url:
        service_data["endpoint"] = url
    
    # Add price if provided
    if price is not None:
        service_data["price"] = price
        service_data["price_unit"] = price_unit
    
    # First, send register message
    register_msg = {
        "type": "register",
        "client_id": client_id,
        "service": service_data,
        "skill_doc": ""  # Optional skill doc
    }
    
    result = asyncio.run(ws_send_and_wait(host, register_msg))
    
    if result and result.get("type") == "registered":
        click.echo(f"✅ Service '{name}' registered successfully!")
        click.echo(f"   ID: {result.get('service_id')}")
        click.echo(f"   Version: {version}")
    else:
        error = result.get("error", "Unknown error") if result else "No response"
        click.echo(f"❌ Failed to register service '{name}': {error}", err=True)
        sys.exit(1)


@cli.command("list")
@click.option("--host", default=DEFAULT_HOST, help="Server host")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def list_services(host: str, output_json: bool):
    """List all registered services"""
    result = asyncio.run(call_api("/api/services"))
    
    if result is None:
        click.echo("❌ Failed to connect to server", err=True)
        sys.exit(1)
    
    services = result.get("services", [])
    
    if output_json:
        click.echo(json.dumps(services, indent=2))
    else:
        if not services:
            click.echo("No services registered.")
            return
        
        click.echo(f"📦 Registered Services ({len(services)}):\n")
        
        for svc in services:
            status_emoji = "🟢" if svc.get("status") == "online" else "🔴"
            click.echo(f"  {status_emoji} {svc.get('name')} (v{svc.get('version')})")
            click.echo(f"     ID: {svc.get('id')}")
            if svc.get("description"):
                click.echo(f"     Description: {svc.get('description')}")
            if svc.get("tags"):
                click.echo(f"     Tags: {', '.join(svc.get('tags', []))}")
            click.echo()


@cli.command()
@click.argument("service")
@click.argument("method")
@click.argument("params", required=False)
@click.option("--host", default=DEFAULT_HOST, help="Server host")
def call(service: str, method: str, params: Optional[str], host: str):
    """Call a service method
    
    SERVICE: Service name or ID
    METHOD: Method name to call
    PARAMS: JSON parameters (optional)
    """
    # Parse params if provided
    call_params = {}
    if params:
        try:
            call_params = json.loads(params)
        except json.JSONDecodeError:
            click.echo(f"❌ Invalid JSON parameters: {params}", err=True)
            sys.exit(1)
    
    client_id = f"cli-{uuid.uuid4().hex[:8]}"
    
    call_msg = {
        "type": "call",
        "client_id": client_id,
        "service": service,
        "method": method,
        "params": call_params,
        "request_id": f"req-{uuid.uuid4().hex[:8]}"
    }
    
    click.echo(f"Calling {service}.{method}...")
    
    result = asyncio.run(ws_send_and_wait(host, call_msg))
    
    if result:
        if result.get("type") == "call_response" and result.get("success"):
            click.echo("✅ Call successful!")
            if result.get("result"):
                click.echo(f"Result: {json.dumps(result.get('result'), indent=2)}")
        else:
            error = result.get("error", "Unknown error")
            click.echo(f"❌ Call failed: {error}", err=True)
    else:
        click.echo("❌ Failed to connect to server", err=True)
        sys.exit(1)


@cli.command()
@click.argument("service_id")
@click.option("--host", default=DEFAULT_HOST, help="Server host")
def unregister(service_id: str, host: str):
    """Unregister a service"""
    click.echo(f"Unregistering service: {service_id}")
    
    # Try via REST API first
    result = asyncio.run(call_api(f"/api/services/{service_id}", method="DELETE"))
    
    if result:
        click.echo(f"✅ Service '{service_id}' unregistered successfully!")
    else:
        # Fall back to WebSocket unregister
        client_id = f"cli-{uuid.uuid4().hex[:8]}"
        unregister_msg = {
            "type": "unregister",
            "client_id": client_id,
            "service_id": service_id
        }
        result = asyncio.run(ws_send_and_wait(host, unregister_msg))
        
        if result and result.get("success"):
            click.echo(f"✅ Service '{service_id}' unregistered successfully!")
        else:
            click.echo(f"❌ Failed to unregister service '{service_id}'", err=True)
            sys.exit(1)


@cli.command()
@click.option("--host", default=DEFAULT_HOST, help="Server host")
def status(host: str):
    """Check server status"""
    result = asyncio.run(call_api("/health"))
    
    if result:
        click.echo("✅ Server is online")
        click.echo(f"   Version: {result.get('version', 'unknown')}")
        click.echo(f"   Services: {result.get('services_count', 0)}")
    else:
        click.echo("❌ Server is offline or not reachable", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()