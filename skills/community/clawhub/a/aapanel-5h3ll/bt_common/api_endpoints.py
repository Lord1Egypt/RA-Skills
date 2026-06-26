# /// script
# dependencies = []
# ///
"""
aaPanel API Endpoint Definitions
Defines all aaPanel API interface paths
"""

# aaPanel minimum version requirement
MIN_PANEL_VERSION = "9.0.0"

# API endpoint definitions
# Format: endpoint_path?action_parameter
API_ENDPOINTS = {
    # System status (composite interface, includes CPU, memory, disk, network, load, etc.)
    "SYSTEM_STATUS": "/system?action=GetNetWork",  # Composite monitoring data interface

    # Logs
    "PANEL_LOGS": "/logs?action=GetLogs",
    "ERROR_LOGS": "/site?action=GetErrorLog",
    "SITE_LOGS": "/site?action=GetSiteLogs",
    "FILE_BODY": "/files?action=GetFileBody",  # Read file content

    # Security
    "FIREWALL_STATUS": "/safe?action=GetFirewallStatus",
    "SECURITY_LOGS": "/safe?action=GetLogs",
    "SSH_INFO": "/safe?action=GetSshInfo",
    "SSH_LOGS": "/mod/ssh/com/get_ssh_list",  # SSH login logs

    # Service management
    "SERVICE_LIST": "/system?action=GetServiceList",
    "SERVICE_STATUS": "/system?action=GetServiceStatus",
    "SOFTWARE_INFO": "/plugin?action=get_soft_find",  # Get software info, parameter sName=service name
    "SOFTWARE_LIST": "/plugin?action=get_soft_list",  # Get software list

    # Website management - PHP projects (traditional sites)
    "SITE_LIST": "/datalist/data/get_data_list",  # requires parameter table=sites

    # Project management - different project types have different endpoints
    "PROJECT_JAVA_LIST": "/mod/java/project/project_list",
    "PROJECT_NODE_LIST": "/project/nodejs/get_project_list",
    "PROJECT_GO_LIST": "/project/go/get_project_list",
    "PROJECT_PYTHON_LIST": "/project/python/GetProjectList",
    "PROJECT_NET_LIST": "/project/net/get_project_list",
    "PROJECT_PROXY_LIST": "/mod/proxy/com/get_list",  # Reverse proxy projects
    "PROJECT_HTML_LIST": "/project/html/get_project_list",  # HTML static projects
    "PROJECT_OTHER_LIST": "/project/other/get_project_list",  # Other projects

    # Database
    "DATABASE_LIST": "/database?action=GetDatabases",

    # SSL certificates
    "SSL_LIST": "/sites?action=GetSsl",
    "SSL_CREATE": "/acme?action=ApplyCert",
    "SSL_RENEW": "/site?action=RenewCert",
    "SSL_REVOKE": "/site?action=CloseSsl",

    # Website management
    "SITE_CREATE": "/site?action=AddSite",
    "SITE_DELETE": "/site?action=DeleteSite",
    "SITE_DOMAIN_ADD": "/site?action=AddDomain",
    "SITE_DOMAIN_DELETE": "/site?action=DeleteDomain",
    "SITE_PHP_VERSION": "/site?action=SetPHPVersion",

    # FTP
    "FTP_LIST": "/ftp?action=GetUserList",
    "FTP_CREATE": "/ftp?action=CreateUser",
    "FTP_DELETE": "/ftp?action=DeleteUser",
    "FTP_SET_PASSWORD": "/ftp?action=SetPassword",

    # Firewall
    "FIREWALL_LIST": "/firewall?action=GetList",
    "FIREWALL_ACCEPT": "/firewall?action=AddAcceptAddress",
    "FIREWALL_DROP": "/firewall?action=AddDropAddress",
    "FIREWALL_DEL": "/firewall?action=DelAddress",

    # Task management
    "TASK_LIST": "/task?action=GetTaskList",
    "CRONTAB_LIST": "/crontab?action=GetCrontab",  # Scheduled task list
    "CRONTAB_LOGS": "/crontab?action=GetLogs",  # Scheduled task logs
}

# API endpoint groups
API_GROUPS = {
    "system": ["SYSTEM_STATUS"],
    "logs": ["PANEL_LOGS", "ERROR_LOGS", "SITE_LOGS", "FILE_BODY"],
    "security": ["FIREWALL_STATUS", "SECURITY_LOGS", "SSH_INFO", "SSH_LOGS"],
    "service": ["SERVICE_LIST", "SERVICE_STATUS", "SOFTWARE_INFO", "SOFTWARE_LIST"],
    "site": ["SITE_LIST", "PROJECT_JAVA_LIST", "PROJECT_NODE_LIST", "PROJECT_GO_LIST", "PROJECT_PYTHON_LIST", "PROJECT_NET_LIST", "PROJECT_PROXY_LIST", "PROJECT_HTML_LIST", "PROJECT_OTHER_LIST"],
    "database": ["DATABASE_LIST"],
    "ssl": ["SSL_LIST", "SSL_CREATE", "SSL_RENEW", "SSL_REVOKE"],
    "ftp": ["FTP_LIST", "FTP_CREATE", "FTP_DELETE"],
    "firewall": ["FIREWALL_LIST", "FIREWALL_ACCEPT", "FIREWALL_DROP"],
    "task": ["TASK_LIST", "CRONTAB_LIST", "CRONTAB_LOGS"],
}

# Endpoint descriptions
API_DESCRIPTIONS = {
    "SYSTEM_STATUS": "Get comprehensive system monitoring data (CPU, memory, disk, network, load, etc.)",
    "PANEL_LOGS": "Get panel operation logs",
    "ERROR_LOGS": "Get error logs",
    "SITE_LOGS": "Get site logs",
    "FILE_BODY": "Read file content (used for reading log files)",
    "FIREWALL_STATUS": "Get firewall status",
    "SECURITY_LOGS": "Get security logs",
    "SSH_INFO": "Get SSH configuration info",
    "SSH_LOGS": "Get SSH login logs",
    "SERVICE_LIST": "Get service list",
    "SERVICE_STATUS": "Get service status",
    "SOFTWARE_INFO": "Get software info (nginx/apache/redis/memcached, etc.)",
    "SOFTWARE_LIST": "Get software list (PHP multi-version query)",
    "SITE_LIST": "Get PHP site list (traditional sites)",
    "PROJECT_JAVA_LIST": "Get Java project list",
    "PROJECT_NODE_LIST": "Get Node.js project list",
    "PROJECT_GO_LIST": "Get Go project list",
    "PROJECT_PYTHON_LIST": "Get Python project list",
    "PROJECT_NET_LIST": "Get .NET project list",
    "PROJECT_PROXY_LIST": "Get reverse proxy project list",
    "PROJECT_HTML_LIST": "Get HTML static project list",
    "PROJECT_OTHER_LIST": "Get other project list",
    "DATABASE_LIST": "Get database list",
    "SSL_LIST": "Get SSL certificate info",
    "SSL_CREATE": "Create Let's Encrypt certificate",
    "SSL_RENEW": "Renew SSL certificate",
    "SSL_REVOKE": "Revoke/disable SSL certificate",
    "SITE_CREATE": "Create new site",
    "SITE_DELETE": "Delete site",
    "SITE_DOMAIN_ADD": "Add domain to site",
    "SITE_DOMAIN_DELETE": "Remove domain from site",
    "SITE_PHP_VERSION": "Set PHP version for site",
    "FTP_LIST": "Get FTP account list",
    "FTP_CREATE": "Create FTP account",
    "FTP_DELETE": "Delete FTP account",
    "FTP_SET_PASSWORD": "Set FTP password",
    "FIREWALL_LIST": "Get firewall rules list",
    "FIREWALL_ACCEPT": "Add IP to whitelist",
    "FIREWALL_DROP": "Add IP to blacklist",
    "FIREWALL_DEL": "Remove IP from firewall",
    "TASK_LIST": "Get task list",
    "CRONTAB_LIST": "Get scheduled task list",
    "CRONTAB_LOGS": "Get scheduled task logs",
}

# Project type mapping
PROJECT_TYPES = {
    "PHP": "SITE_LIST",
    "Java": "PROJECT_JAVA_LIST",
    "Node": "PROJECT_NODE_LIST",
    "Go": "PROJECT_GO_LIST",
    "Python": "PROJECT_PYTHON_LIST",
    "net": "PROJECT_NET_LIST",
    "Proxy": "PROJECT_PROXY_LIST",
    "HTML": "PROJECT_HTML_LIST",
    "Other": "PROJECT_OTHER_LIST",
}

# Services that can be queried for status (via SOFTWARE_INFO interface)
SOFTWARE_SERVICES = ["nginx", "apache", "mysql", "pure-ftpd", "redis", "memcached"]

# PHP version list (service name format: php-X.X, e.g., php-8.2, php-7.4)
# Note: PHP supports multiple versions coexisting, one server may have multiple versions installed
# Query using get_soft_list interface, the returned name field matches the service name exactly
PHP_VERSIONS = ["8.5", "8.4", "8.3", "8.2", "8.1", "8.0", "7.4", "7.3", "7.2", "7.1", "7.0", "5.6", "5.5", "5.4", "5.3", "5.2"]

# Service log paths (read via FILE_BODY interface)
# Note: Only installed and running services have readable logs
SERVICE_LOG_PATHS = {
    "nginx": "/www/server/nginx/logs/error.log",
    "apache": "/www/wwwlogs/error_log",
    "redis": "/www/server/redis/redis.log",
    # mysql uses a special interface, not file path
    # memcached has no standard log file
}

# MySQL log interfaces
MYSQL_LOG_APIS = {
    "error": "/database?action=GetErrorLog",      # MySQL error logs
    "slow": "/database?action=GetSlowLogs",       # MySQL slow query logs
}

# Special service APIs (requires plugin-supported database services)
SPECIAL_SERVICE_APIS = {
    "pgsql": {
        "status": "/plugin?action=a&name=pgsql_manager&s=get_service",
        "log": "/plugin?action=a&name=pgsql_manager&s=get_pgsql_log",
        "slow_log": "/plugin?action=a&name=pgsql_manager&s=get_slow_pgsql_log",
    },
    "mysql": {
        "log": "/database?action=GetErrorLog",
        "slow_log": "/database?action=GetSlowLogs",
    }
}


def get_endpoint(name: str) -> str:
    """
    Get API endpoint path

    Args:
        name: Endpoint name

    Returns:
        Endpoint path

    Raises:
        KeyError: Endpoint not found
    """
    if name not in API_ENDPOINTS:
        raise KeyError(f"API endpoint not found: {name}")
    return API_ENDPOINTS[name]


def get_endpoints_by_group(group: str) -> dict:
    """
    Get all endpoints in a group

    Args:
        group: Group name

    Returns:
        Endpoint dictionary
    """
    if group not in API_GROUPS:
        return {}
    return {name: API_ENDPOINTS[name] for name in API_GROUPS[group]}


def list_endpoints() -> dict:
    """
    List all endpoints

    Returns:
        Endpoint dictionary
    """
    return API_ENDPOINTS.copy()


def get_endpoint_description(name: str) -> str:
    """
    Get endpoint description

    Args:
        name: Endpoint name

    Returns:
        Endpoint description
    """
    return API_DESCRIPTIONS.get(name, "Unknown endpoint")
