# /// script
# dependencies = [
#   "requests>=2.28",
#   "pyyaml>=6.0",
# ]
# ///
"""
aaPanel API Client
Supports multi-server management and API request encapsulation
"""

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .api_endpoints import API_ENDPOINTS, MIN_PANEL_VERSION, get_endpoint


def sign_request(token: str, params: Optional[dict] = None) -> dict:
    """
    Generate API request signature
    aaPanel API uses MD5(time + MD5(token)) signature mechanism

    Args:
        token: aaPanel API token
        params: Request parameters

    Returns:
        Complete parameters including signature
    """
    if params is None:
        params = {}

    request_time = int(time.time())
    # Signature algorithm: request_token = md5(request_time + md5(token))
    token_md5 = hashlib.md5(token.encode()).hexdigest()
    request_token = hashlib.md5(f"{request_time}{token_md5}".encode()).hexdigest()

    return {
        **params,
        "request_time": request_time,
        "request_token": request_token,
    }


@dataclass
class ServerConfig:
    """Server config"""

    name: str
    host: str
    token: str
    timeout: int = 10000
    enabled: bool = True


@dataclass
class BtClient:
    """
    aaPanel client class

    Attributes:
        name: Server name
        host: Panel address
        token: API Token
        timeout: Request timeout (milliseconds)
        verify_ssl: Whether to verify SSL certificate
    """

    name: str
    host: str
    token: str
    timeout: int = 10000
    enabled: bool = True
    verify_ssl: bool = True  # SSL verification toggle
    _session: requests.Session = field(default=None, repr=False, compare=False)  # type: ignore

    def __post_init__(self):
        # Remove trailing slash
        self.host = self.host.rstrip("/")
        # Create session
        self._session = requests.Session()
        # Configure retry strategy
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)
        # Set default headers
        self._session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"}
        )
        # Set SSL verification (based on config)
        self._session.verify = self.verify_ssl

    def request(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """
        Send API request

        Args:
            endpoint: API endpoint
            params: Request parameters

        Returns:
            API response data

        Raises:
            ConnectionError: Cannot connect to server
            TimeoutError: Request timeout
            RuntimeError: API request failed
        """
        signed_params = sign_request(self.token, params)
        url = f"{self.host}{endpoint}"

        try:
            response = self._session.post(
                url,
                data=urlencode(signed_params),
                timeout=self.timeout / 1000,
            )
            response.raise_for_status()
            data = response.json()

            # Check aaPanel API response status
            # Note: Some APIs return a list instead of a dictionary
            if isinstance(data, dict) and data.get("status") is False:
                raise RuntimeError(data.get("msg", "API request failed"))

            return data

        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Cannot connect to server: {self.host}")
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timeout: {self.host}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")

    def get_system_status(self) -> dict:
        """
        Get comprehensive system monitoring data
        Includes CPU, memory, disk, network, load, system info, etc.

        Returns:
            Raw monitoring data
        """
        return self.request(API_ENDPOINTS["SYSTEM_STATUS"])

    def get_service_list(self) -> list:
        """Get service list"""
        result = self.request(API_ENDPOINTS["SERVICE_LIST"])
        if not isinstance(result, dict):
            return result if isinstance(result, list) else []
        # aaPanel API may return status=false error response
        if result.get("status") is False:
            return []
        return result.get("data", [])

    def get_site_list(self, page: int = 1, limit: int = 100) -> list:
        """
        Get PHP site list (traditional sites)

        Args:
            page: Page number
            limit: Items per page
        """
        params = {"type": "-1", "search": "", "p": page, "limit": limit, "table": "sites", "order": ""}
        result = self.request(API_ENDPOINTS["SITE_LIST"], params)
        return result.get("data", []) if isinstance(result, dict) else []

    def get_project_list(self, project_type: str, page: int = 1, limit: int = 100) -> list:
        """
        Get project list (Java/Node/Go/Python/.NET/Proxy/HTML/Other)

        Args:
            project_type: Project type (Java/Node/Go/Python/net/Proxy/HTML/Other)
            page: Page number
            limit: Items per page
        """
        from .api_endpoints import PROJECT_TYPES

        endpoint_key = PROJECT_TYPES.get(project_type)
        if not endpoint_key:
            raise ValueError(f"Unsupported project type: {project_type}, supported types: {list(PROJECT_TYPES.keys())}")

        endpoint = API_ENDPOINTS[endpoint_key]
        params = {"search": "", "p": page, "limit": limit, "type_id": ""}
        result = self.request(endpoint, params)
        return result.get("data", []) if isinstance(result, dict) else []

    def get_all_sites(self) -> list:
        """
        Get all sites and project lists

        Returns:
            List of all sites, including different project types
        """
        all_sites = []

        # Get PHP sites
        php_sites = self.get_site_list()
        for site in php_sites:
            site["_source"] = "PHP"
            all_sites.append(site)

        # Get projects of each type (Java/Node/Go/Python/net/Proxy/HTML/Other)
        for project_type in ["Java", "Node", "Go", "Python", "net", "Proxy", "HTML", "Other"]:
            try:
                projects = self.get_project_list(project_type)
                for proj in projects:
                    proj["_source"] = project_type
                    all_sites.append(proj)
            except Exception:
                # Ignore errors fetching individual types
                pass

        return all_sites

    def get_database_list(self) -> list:
        """Get database list"""
        result = self.request(API_ENDPOINTS["DATABASE_LIST"])
        return result if isinstance(result, list) else result.get("data", [])

    def get_ssl_info(self, site_name: str) -> dict:
        """
        Get SSL certificate info for a site.

        Args:
            site_name: Site name

        Returns:
            SSL certificate info
        """
        params = {"siteName": site_name}
        return self.request(API_ENDPOINTS["SSL_LIST"], params)

    def provision_letsencrypt(self, site_name: str, dns_type: str = "dns") -> dict:
        """
        Provision Let's Encrypt certificate.

        Args:
            site_name: Site name
            dns_type: DNS verification type (dns/dns_ali/dns_cloudflare etc)

        Returns:
            Result of provision operation
        """
        params = {
            "siteName": site_name,
            "type": dns_type,
            "dnspars": ""
        }
        return self.request(API_ENDPOINTS["SSL_CREATE"], params)

    def renew_ssl(self, site_name: str) -> dict:
        """
        Renew SSL certificate for a site.

        Args:
            site_name: Site name

        Returns:
            Result of renewal operation
        """
        params = {"siteName": site_name}
        return self.request(API_ENDPOINTS["SSL_RENEW"], params)

    def revoke_ssl(self, site_name: str) -> dict:
        """
        Revoke/disable SSL certificate.

        Args:
            site_name: Site name

        Returns:
            Result of revoke operation
        """
        params = {"siteName": site_name}
        return self.request(API_ENDPOINTS["SSL_REVOKE"], params)

    def create_site(self, name: str, path: str, php_version: str = "74") -> dict:
        """
        Create a new site.

        Args:
            name: Site name (domain)
            path: Document root path
            php_version: PHP version (default: "74")

        Returns:
            Result of creation operation
        """
        import json
        webname = json.dumps({
            "siteinfo": {
                "name": name,
                "domain": name,
                "path": path,
                "type": 0,
                "php_version": php_version
            }
        })
        params = {"webname": webname}
        return self.request(API_ENDPOINTS["SITE_CREATE"], params)

    def delete_site(self, site_id: int) -> dict:
        """
        Delete a site.

        Args:
            site_id: Site ID

        Returns:
            Result of deletion operation
        """
        params = {"id": site_id}
        return self.request(API_ENDPOINTS["SITE_DELETE"], params)

    def add_domain(self, site_name: str, domain: str, port: int = 80) -> dict:
        """
        Add domain to a site.

        Args:
            site_name: Site name
            domain: Domain to add
            port: Port (default: 80)

        Returns:
            Result of add operation
        """
        params = {
            "siteName": site_name,
            "domain": domain,
            "id": 1,
            "port": port
        }
        return self.request(API_ENDPOINTS["SITE_DOMAIN_ADD"], params)

    def remove_domain(self, site_name: str, domain: str, port: int = 80) -> dict:
        """
        Remove domain from a site.

        Args:
            site_name: Site name
            domain: Domain to remove
            port: Port (default: 80)

        Returns:
            Result of remove operation
        """
        params = {
            "siteName": site_name,
            "domain": domain,
            "port": port
        }
        return self.request(API_ENDPOINTS["SITE_DOMAIN_DELETE"], params)

    def set_php_version(self, site_name: str, version: str) -> dict:
        """
        Set PHP version for a site.

        Args:
            site_name: Site name
            version: PHP version (e.g., "74", "83")

        Returns:
            Result of operation
        """
        params = {"siteName": site_name, "version": version}
        return self.request(API_ENDPOINTS["SITE_PHP_VERSION"], params)

    def get_ftp_list(self) -> list:
        """
        Get FTP account list.

        Returns:
            List of FTP accounts
        """
        result = self.request(API_ENDPOINTS["FTP_LIST"])
        return result if isinstance(result, list) else result.get("data", [])

    def create_ftp_user(self, username: str, password: str, path: str,
                       active: bool = True) -> dict:
        """
        Create FTP account.

        Args:
            username: FTP username
            password: FTP password
            path: Home directory
            active: Whether account is active

        Returns:
            Result of creation operation
        """
        params = {
            "ftp_username": username,
            "ftp_password": password,
            "path": path,
            "active": "true" if active else "false"
        }
        return self.request(API_ENDPOINTS["FTP_CREATE"], params)

    def delete_ftp_user(self, user_id: int) -> dict:
        """
        Delete FTP account.

        Args:
            user_id: FTP account ID

        Returns:
            Result of deletion operation
        """
        params = {"id": user_id}
        return self.request(API_ENDPOINTS["FTP_DELETE"], params)

    def set_ftp_password(self, user_id: int, password: str) -> dict:
        """
        Set FTP account password.

        Args:
            user_id: FTP account ID
            password: New password

        Returns:
            Result of operation
        """
        params = {"id": user_id, "password": password}
        return self.request(API_ENDPOINTS["FTP_SET_PASSWORD"], params)

    def get_firewall_list(self) -> list:
        """
        Get firewall rules list.

        Returns:
            List of firewall rules
        """
        result = self.request(API_ENDPOINTS["FIREWALL_LIST"])
        return result if isinstance(result, list) else result.get("data", [])

    def add_ip_whitelist(self, ip_address: str) -> dict:
        """
        Add IP to whitelist.

        Args:
            ip_address: IP address

        Returns:
            Result of operation
        """
        params = {"address": ip_address}
        return self.request(API_ENDPOINTS["FIREWALL_ACCEPT"], params)

    def add_ip_blacklist(self, ip_address: str) -> dict:
        """
        Add IP to blacklist.

        Args:
            ip_address: IP address

        Returns:
            Result of operation
        """
        params = {"address": ip_address}
        return self.request(API_ENDPOINTS["FIREWALL_DROP"], params)

    def remove_ip_firewall(self, ip_address: str) -> dict:
        """
        Remove IP from firewall.

        Args:
            ip_address: IP address

        Returns:
            Result of operation
        """
        params = {"address": ip_address}
        return self.request(API_ENDPOINTS["FIREWALL_DEL"], params)

    def get_firewall_status(self) -> dict:
        """Get firewall status"""
        return self.request(API_ENDPOINTS["FIREWALL_STATUS"])

    def get_security_logs(self, page: int = 1, limit: int = 20) -> dict:
        """
        Get security logs

        Args:
            page: Page number
            limit: Items per page
        """
        return self.request(API_ENDPOINTS["SECURITY_LOGS"], {"page": page, "limit": limit})

    def get_ssh_info(self) -> dict:
        """Get SSH info"""
        return self.request(API_ENDPOINTS["SSH_INFO"])

    def get_ssh_logs(self, page: int = 1, limit: int = 20, search: str = "",
                     login_type: str = "ALL") -> dict:
        """
        Get SSH login logs

        Args:
            page: Page number
            limit: Items per page
            search: Search keyword (IP address or username)
            login_type: Login type filter (ALL/password/key)

        Returns:
            SSH login log list
        """
        params = {
            "search": search,
            "p": page,
            "limit": limit,
            "select": "ALL",
            "historyType": "ALL",
        }
        result = self.request(API_ENDPOINTS["SSH_LOGS"], params)
        return result if isinstance(result, dict) else {"data": result}

    def get_panel_logs(self, page: int = 1, limit: int = 20) -> dict:
        """
        Get panel operation logs

        Args:
            page: Page number
            limit: Items per page
        """
        return self.request(API_ENDPOINTS["PANEL_LOGS"], {"page": page, "limit": limit})

    def get_error_logs(self, site_name: str) -> dict:
        """
        Get error logs

        Args:
            site_name: Site name
        """
        return self.request(API_ENDPOINTS["ERROR_LOGS"], {"siteName": site_name})

    def get_task_list(self) -> dict:
        """Get task list"""
        return self.request(API_ENDPOINTS["TASK_LIST"])

    def get_software_info(self, name: str) -> dict:
        """
        Get software/service info

        Args:
            name: Service name (nginx/apache/redis/memcached/pure-ftpd, etc.)

        Returns:
            Software info, including version, status, whether installed, etc.
        """
        params = {"sName": name}
        return self.request(API_ENDPOINTS["SOFTWARE_INFO"], params)

    def get_php_versions(self) -> list:
        """
        Get installed PHP version list

        Returns:
            List of installed PHP version info
        """
        params = {"type": -1, "query": "php", "p": 1, "row": 30, "force": 0}
        result = self.request(API_ENDPOINTS["SOFTWARE_LIST"], params)
        return result.get("list", []) if isinstance(result, dict) else []

    def get_file_body(self, path: str) -> dict:
        """
        Read file content (used for reading log files)

        Args:
            path: File path

        Returns:
            File content info
        """
        params = {"path": path}
        return self.request(API_ENDPOINTS["FILE_BODY"], params)

    def get_service_log(self, service: str, log_type: str = "error") -> dict:
        """
        Get service logs

        Note: Only installed and running services have readable logs.
        Check the service's installed status before calling.

        Args:
            service: Service name (nginx/apache/redis/mysql/pgsql)
            log_type: Log type (error/slow)

        Returns:
            Log content
        """
        from .api_endpoints import SERVICE_LOG_PATHS, SPECIAL_SERVICE_APIS

        # Handle special services (pgsql, mysql)
        if service in SPECIAL_SERVICE_APIS:
            api_key = "log" if log_type == "error" else "slow_log"
            endpoint = SPECIAL_SERVICE_APIS[service].get(api_key)
            if endpoint:
                return self.request(endpoint)
            return {"status": False, "msg": f"Unsupported log type: {log_type}"}

        # Standard service log paths (nginx, apache, redis)
        if service in SERVICE_LOG_PATHS:
            log_path = SERVICE_LOG_PATHS[service]
            return self.get_file_body(log_path)

        return {"status": False, "msg": f"Unsupported service: {service}"}

    def get_service_status(self, service: str) -> dict:
        """
        Get single service status

        Args:
            service: Service name (nginx/apache/redis/memcached/pure-ftpd/pgsql/php-x.x)

        Returns:
            Service status info
        """
        from .api_endpoints import SPECIAL_SERVICE_APIS

        # Handle special services (pgsql)
        if service == "pgsql":
            endpoint = SPECIAL_SERVICE_APIS["pgsql"]["status"]
            result = self.request(endpoint)
            if result.get("status") and "data" in result:
                # Parse pgsql status format: {"data": ["enabled", 1], "status": true}
                data = result.get("data", [])
                return {
                    "name": service,
                    "title": "PostgreSQL",
                    "status": data[1] == 1 if len(data) > 1 else False,
                    "status_text": data[0] if len(data) > 0 else "Unknown",
                    "installed": True,
                }
            return {"name": service, "status": False, "installed": False}

        # Standard services queried via software interface
        info = self.get_software_info(service)
        if isinstance(info, dict):
            return {
                "name": service,
                "title": info.get("title", service),
                "version": info.get("version", ""),
                "status": info.get("status", False),
                "installed": info.get("setup", False),
                "pid": info.get("pid", 0),
            }
        return {"name": service, "status": False, "installed": False}

    def get_all_services_status(self, services: Optional[list] = None) -> list:
        """
        Get all services status

        Args:
            services: List of services to query, defaults to all services when None

        Returns:
            Service status list
        """
        from .api_endpoints import SOFTWARE_SERVICES

        if services is None:
            services = SOFTWARE_SERVICES.copy()

        results = []

        # Query standard services
        for service in services:
            try:
                status = self.get_service_status(service)
                results.append(status)
            except Exception as e:
                results.append({
                    "name": service,
                    "status": False,
                    "installed": False,
                    "error": str(e),
                })

        # Query installed PHP versions
        try:
            php_list = self.get_php_versions()
            for php_info in php_list:
                name = php_info.get("name", "")
                if name.startswith("php-"):
                    results.append({
                        "name": name,
                        "title": php_info.get("title", name),
                        "version": php_info.get("version", ""),
                        "status": php_info.get("status", False),
                        "installed": php_info.get("setup", False),
                        "pid": php_info.get("pid", 0),
                    })
        except Exception:
            pass

        # Query pgsql (if installed)
        try:
            pgsql_status = self.get_service_status("pgsql")
            if pgsql_status.get("installed"):
                results.append(pgsql_status)
        except Exception:
            pass

        return results

    def get_crontab_list(self, page: int = 1, limit: int = 100, search: str = "") -> dict:
        """
        Get scheduled task list

        Args:
            page: Page number
            limit: Items per page
            search: Search keyword

        Returns:
            Scheduled task list
        """
        params = {"p": page, "count": limit, "search": search, "type_id": "", "order_param": ""}
        result = self.request(API_ENDPOINTS["CRONTAB_LIST"], params)
        return result if isinstance(result, dict) else {"data": result}

    def get_crontab_logs(self, task_id: int, start_timestamp: Optional[int] = None,
                         end_timestamp: Optional[int] = None) -> dict:
        """
        Get scheduled task logs

        Args:
            task_id: Task ID
            start_timestamp: Start timestamp
            end_timestamp: End timestamp

        Returns:
            Task logs
        """
        params = {"id": task_id}
        if start_timestamp:
            params["start_timestamp"] = start_timestamp
        if end_timestamp:
            params["end_timestamp"] = end_timestamp
        return self.request(API_ENDPOINTS["CRONTAB_LOGS"], params)

    def health_check(self) -> bool:
        """
        Health check

        Returns:
            Whether connection successful
        """
        try:
            self.get_system_status()
            return True
        except Exception:
            return False

    def close(self):
        """Close connection"""
        self._session.close()


class BtClientManager:
    """Multi-server manager"""

    def __init__(self):
        self.clients: dict[str, BtClient] = {}
        self.config: Optional[dict] = None
        self.global_config: dict = {
            "retryCount": 3,
            "retryDelay": 1000,
            "concurrency": 3,
            "thresholds": {"cpu": 80, "memory": 85, "disk": 90},
        }

    def load_config(self, config_path: Optional[str] = None) -> "BtClientManager":
        """
        Load servers from config file

        Args:
            config_path: Config file path

        Returns:
            self, supports method chaining
        """
        from .config import load_config

        self.config = load_config(config_path)

        # Load global config
        if "global" in self.config:
            self.global_config.update(self.config["global"])

        # Initialize all server clients
        for server in self.config.get("servers", []):
            if server.get("enabled", True):
                client = BtClient(
                    name=server["name"],
                    host=server["host"],
                    token=server["token"],
                    timeout=server.get("timeout", 10000),
                    verify_ssl=server.get("verify_ssl", True),  # Pass SSL verification config
                )
                self.clients[server["name"]] = client

        return self

    def get_global_config(self) -> dict:
        """Get global config"""
        return self.global_config

    def get_client(self, name: str) -> BtClient:
        """
        Get client

        Args:
            name: Server name

        Returns:
            aaPanel client instance

        Raises:
            KeyError: Server not found
        """
        if name not in self.clients:
            raise KeyError(f"Server not found: {name}")
        return self.clients[name]

    def get_all_clients(self) -> dict[str, BtClient]:
        """Get all clients"""
        return self.clients

    def add_server(self, config: dict) -> BtClient:
        """
        Add server

        Args:
            config: Server configuration
        """
        client = BtClient(
            name=config["name"],
            host=config["host"],
            token=config["token"],
            timeout=config.get("timeout", 10000),
            verify_ssl=config.get("verify_ssl", True),  # Pass SSL verification config
        )
        self.clients[config["name"]] = client
        return client

    def remove_server(self, name: str):
        """
        Remove server

        Args:
            name: Server name
        """
        if name in self.clients:
            self.clients[name].close()
            del self.clients[name]

    def get_server_list(self) -> list[str]:
        """Get server list"""
        return list(self.clients.keys())

    def execute_all(self, action) -> dict[str, Any]:
        """
        Execute action on all servers in parallel

        Args:
            action: Async action function, receives BtClient parameter

        Returns:
            Execution results for each server
        """
        results = {}
        for name, client in self.clients.items():
            try:
                result = action(client)
                results[name] = {"success": True, "data": result}
            except Exception as e:
                results[name] = {"success": False, "error": str(e)}
        return results

    def check_all_connections(self) -> dict[str, bool]:
        """Check all server connection status"""
        return {name: client.health_check() for name, client in self.clients.items()}

    def close_all(self):
        """Close all connections"""
        for client in self.clients.values():
            client.close()
