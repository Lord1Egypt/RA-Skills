"""
Basic usage examples for api-mock-server
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from mock_server import MockServer


def example_static_routes():
    """Define static JSON response routes."""
    server = MockServer(port=3001)
    
    server.get("/users", {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    })
    
    server.get("/health", {"status": "ok"})
    
    print("Static routes defined on port 3001")
    print("GET /users -> list of users")
    print("GET /health -> health check")
    # server.start()  # Uncomment to actually run


def example_dynamic_routes():
    """Define dynamic routes with path parameters."""
    server = MockServer(port=3002)
    
    def get_user(req):
        user_id = req.params.get("id", "unknown")
        return {
            "id": user_id,
            "name": f"User_{user_id}",
            "email": f"user_{user_id}@example.com"
        }
    
    server.get("/users/{id}", get_user)
    
    print("Dynamic routes defined on port 3002")
    print("GET /users/123 -> user details for id=123")


def example_post_with_validation():
    """POST route with request body validation."""
    server = MockServer(port=3003)
    
    schema = {
        "type": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "email": {"type": "string", "format": "email"}
        }
    }
    
    def create_user(req):
        return {
            "id": 123,
            "name": req.body.get("name"),
            "email": req.body.get("email"),
            "created": True
        }
    
    server.post("/users", create_user, validate_schema=schema)
    
    print("POST /users with validation defined on port 3003")


def example_config_file():
    """Load routes from a JSON config file."""
    config = {
        "port": 3004,
        "latency": 100,
        "routes": [
            {
                "method": "GET",
                "path": "/products",
                "response": {
                    "products": [
                        {"sku": "A001", "name": "Widget", "price": 9.99}
                    ]
                }
            },
            {
                "method": "POST",
                "path": "/orders",
                "validate": {
                    "required": ["product_id", "quantity"],
                    "properties": {
                        "product_id": {"type": "string"},
                        "quantity": {"type": "integer", "minimum": 1}
                    }
                },
                "response": {"order_id": "ORD-12345", "status": "confirmed"}
            }
        ]
    }
    
    import json
    with open("/tmp/mock-config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    server = MockServer.from_config("/tmp/mock-config.json")
    print("Server loaded from config file on port 3004")
    print(f"Config: {json.dumps(config, indent=2)}")
    
    os.remove("/tmp/mock-config.json")


if __name__ == "__main__":
    print("=" * 50)
    print("Example 1: Static Routes")
    print("=" * 50)
    example_static_routes()
    
    print("\n" + "=" * 50)
    print("Example 2: Dynamic Routes")
    print("=" * 50)
    example_dynamic_routes()
    
    print("\n" + "=" * 50)
    print("Example 3: POST with Validation")
    print("=" * 50)
    example_post_with_validation()
    
    print("\n" + "=" * 50)
    print("Example 4: Config File")
    print("=" * 50)
    example_config_file()
