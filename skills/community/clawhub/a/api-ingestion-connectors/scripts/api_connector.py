#!/usr/bin/env python3
"""
API Connector implementation for api-ingestion-connectors skill.
Provides core functionality for connecting to external APIs and ingesting data.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class APIType(Enum):
    """Types of API connectors."""
    REST = "rest"
    GRAPHQL = "graphql"
    SOAP = "soap"


class AuthType(Enum):
    """Authentication methods."""
    NONE = "none"
    API_KEY = "api_key"
    BEARER = "bearer"
    BASIC = "basic"
    OAUTH2 = "oauth2"


class PaginationType(Enum):
    """Pagination strategies."""
    NONE = "none"
    OFFSET = "offset"
    PAGE = "page"
    CURSOR = "cursor"
    LINK = "link"


@dataclass
class AuthConfig:
    """Authentication configuration."""
    auth_type: AuthType = AuthType.NONE
    token: Optional[str] = None
    api_key: Optional[str] = None
    api_key_header: str = "X-API-Key"
    username: Optional[str] = None
    password: Optional[str] = None
    oauth_token_endpoint: Optional[str] = None
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None


@dataclass
class PaginationConfig:
    """Pagination configuration."""
    pagination_type: PaginationType = PaginationType.NONE
    page_size: int = 20
    start_at: int = 0
    offset_param: str = "offset"
    limit_param: str = "limit"
    page_param: str = "page"
    cursor_param: str = "after"
    next_cursor_field: Optional[str] = None
    has_next_field: Optional[str] = None


@dataclass
class APIRequest:
    """Represents an API request."""
    endpoint: str
    method: str = "GET"
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    body: Optional[Union[Dict, str]] = None
    timeout: int = 30


@dataclass
class TransformationRule:
    """Data transformation rule."""
    source_field: str
    target_field: str
    node_type: Optional[str] = None
    transform_func: Optional[callable] = None


class APIConnector:
    """Core API connector for ingesting data from external APIs."""

    def __init__(self, name: str, api_type: APIType = APIType.REST,
                 endpoint: str = "", method: str = "GET"):
        """Initialize API connector."""
        self.name = name
        self.api_type = api_type
        self.endpoint = endpoint
        self.method = method
        self.auth_config = AuthConfig()
        self.pagination_config = PaginationConfig()
        self.request_headers: Dict[str, str] = {}
        self.request_params: Dict[str, Any] = {}
        self.request_body: Optional[Union[Dict, str]] = None
        self.transformations: List[TransformationRule] = []
        self.response_data: Optional[Union[Dict, List]] = None
        self.fetched_at: Optional[datetime] = None
        self.total_records: int = 0
        self.errors: List[str] = []

    def set_auth(self, auth_type: str, **kwargs) -> None:
        """Configure authentication."""
        self.auth_config.auth_type = AuthType(auth_type)

        if auth_type == "api_key":
            self.auth_config.api_key = kwargs.get("api_key")
            self.auth_config.api_key_header = kwargs.get("header", "X-API-Key")
        elif auth_type == "bearer":
            self.auth_config.token = kwargs.get("token")
        elif auth_type == "basic":
            self.auth_config.username = kwargs.get("username")
            self.auth_config.password = kwargs.get("password")
        elif auth_type == "oauth2":
            self.auth_config.oauth_token_endpoint = kwargs.get("token_endpoint")
            self.auth_config.oauth_client_id = kwargs.get("client_id")
            self.auth_config.oauth_client_secret = kwargs.get("client_secret")

    def set_pagination(self, pagination_type: str, **kwargs) -> None:
        """Configure pagination."""
        self.pagination_config.pagination_type = PaginationType(pagination_type)
        self.pagination_config.page_size = kwargs.get("page_size", 20)
        self.pagination_config.start_at = kwargs.get("start_at", 0)

        if pagination_type == "offset":
            self.pagination_config.offset_param = kwargs.get("param_offset", "offset")
            self.pagination_config.limit_param = kwargs.get("param_limit", "limit")
        elif pagination_type == "page":
            self.pagination_config.page_param = kwargs.get("param", "page")
        elif pagination_type == "cursor":
            self.pagination_config.cursor_param = kwargs.get("param", "after")
            self.pagination_config.next_cursor_field = kwargs.get("next_cursor_field")
            self.pagination_config.has_next_field = kwargs.get("has_next_field")

    def set_headers(self, headers: Dict[str, str]) -> None:
        """Set request headers."""
        self.request_headers.update(headers)

    def set_params(self, params: Dict[str, Any]) -> None:
        """Set request parameters."""
        self.request_params.update(params)

    def set_body(self, body: Union[Dict, str]) -> None:
        """Set request body."""
        self.request_body = body

    def add_transformation(self, source: str, target: str, 
                          node_type: Optional[str] = None) -> None:
        """Add data transformation rule."""
        rule = TransformationRule(
            source_field=source,
            target_field=target,
            node_type=node_type
        )
        self.transformations.append(rule)

    def get_request_config(self) -> APIRequest:
        """Build complete request configuration."""
        headers = dict(self.request_headers)

        # Add authentication headers
        if self.auth_config.auth_type == AuthType.API_KEY:
            headers[self.auth_config.api_key_header] = self.auth_config.api_key or ""
        elif self.auth_config.auth_type == AuthType.BEARER:
            headers["Authorization"] = f"Bearer {self.auth_config.token}"
        elif self.auth_config.auth_type == AuthType.BASIC:
            import base64
            credentials = f"{self.auth_config.username}:{self.auth_config.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"

        return APIRequest(
            endpoint=self.endpoint,
            method=self.method,
            headers=headers,
            params=dict(self.request_params),
            body=self.request_body
        )

    def build_pagination_params(self, page: int) -> Dict[str, Any]:
        """Build pagination parameters for current page."""
        params = {}

        if self.pagination_config.pagination_type == PaginationType.OFFSET:
            offset = self.pagination_config.start_at + (page * self.pagination_config.page_size)
            params[self.pagination_config.offset_param] = offset
            params[self.pagination_config.limit_param] = self.pagination_config.page_size

        elif self.pagination_config.pagination_type == PaginationType.PAGE:
            page_num = self.pagination_config.start_at + page
            params[self.pagination_config.page_param] = page_num

        return params

    def transform_to_graph(self, data: Union[Dict, List], 
                          node_type: str = "Entity") -> Dict[str, List]:
        """Transform API response data to graph format."""
        nodes = []
        edges = []

        # Handle list of items
        if isinstance(data, list):
            for i, item in enumerate(data):
                node = self._transform_item_to_node(item, node_type, i)
                if node:
                    nodes.append(node)
        # Handle single object
        elif isinstance(data, dict):
            node = self._transform_item_to_node(data, node_type, 0)
            if node:
                nodes.append(node)

        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_records": len(nodes),
                "connector": self.name,
                "api_type": self.api_type.value,
                "timestamp": datetime.now().isoformat()
            }
        }

    def _transform_item_to_node(self, item: Dict, node_type: str, 
                               index: int) -> Optional[Dict]:
        """Transform single item to graph node."""
        if not isinstance(item, dict):
            return None

        # Use id or generate one
        node_id = item.get("id") or f"{self.name}_{node_type}_{index}"

        properties = {}
        for rule in self.transformations:
            if rule.source_field in item:
                properties[rule.target_field] = item[rule.source_field]

        # If no transformations, use all fields
        if not properties:
            properties = dict(item)

        return {
            "id": node_id,
            "type": node_type,
            "properties": properties
        }

    def validate_config(self) -> bool:
        """Validate connector configuration."""
        if not self.endpoint:
            self.errors.append("Endpoint is required")
            return False

        if self.api_type == APIType.REST and not self.method:
            self.errors.append("HTTP method is required for REST API")
            return False

        return len(self.errors) == 0

    def get_summary(self) -> Dict:
        """Get connector configuration summary."""
        return {
            "name": self.name,
            "api_type": self.api_type.value,
            "endpoint": self.endpoint,
            "method": self.method,
            "auth_type": self.auth_config.auth_type.value,
            "pagination_type": self.pagination_config.pagination_type.value,
            "page_size": self.pagination_config.page_size,
            "transformations_count": len(self.transformations),
            "total_records_fetched": self.total_records,
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
            "errors": self.errors
        }

    def print_config(self) -> None:
        """Print connector configuration."""
        print(f"\n{'='*60}")
        print(f"API CONNECTOR: {self.name}")
        print(f"{'='*60}")
        print(f"API Type: {self.api_type.value}")
        print(f"Endpoint: {self.endpoint}")
        print(f"Method: {self.method}")
        print(f"Auth Type: {self.auth_config.auth_type.value}")
        print(f"Pagination: {self.pagination_config.pagination_type.value}")

        if self.request_params:
            print(f"\nQuery Parameters:")
            for key, value in self.request_params.items():
                print(f"  {key}: {value}")

        if self.transformations:
            print(f"\nTransformations ({len(self.transformations)}):")
            for t in self.transformations:
                print(f"  {t.source_field} → {t.target_field}")


if __name__ == "__main__":
    # Example 1: REST API with Bearer token
    rest_connector = APIConnector(
        name="github_users",
        api_type=APIType.REST,
        endpoint="https://api.github.com/users",
        method="GET"
    )
    rest_connector.set_auth("bearer", token="your_token_here")
    rest_connector.set_pagination("page", page_size=30, start_at=1)
    rest_connector.add_transformation("login", "username")
    rest_connector.add_transformation("id", "github_id")
    rest_connector.add_transformation("type", "user_type")

    print("Example 1: REST API Connector")
    rest_connector.print_config()

    # Example 2: GraphQL connector
    graphql_connector = APIConnector(
        name="github_repos",
        api_type=APIType.GRAPHQL,
        endpoint="https://api.github.com/graphql",
        method="POST"
    )
    graphql_connector.set_auth("bearer", token="your_token_here")
    graphql_connector.set_body("""
    query {
      search(first: 10, query: "language:python stars:>1000", type: REPOSITORY) {
        edges {
          node {
            name
            owner { login }
            stargazerCount
          }
        }
      }
    }
    """)
    graphql_connector.add_transformation("name", "repo_name")
    graphql_connector.add_transformation("stargazerCount", "stars")

    print("\nExample 2: GraphQL Connector")
    graphql_connector.print_config()

    # Example 3: API Key authentication with offset pagination
    api_key_connector = APIConnector(
        name="shopify_products",
        api_type=APIType.REST,
        endpoint="https://shop.myshopify.com/admin/api/2024-01/products.json",
        method="GET"
    )
    api_key_connector.set_auth("api_key", 
                               api_key="your_api_key_here",
                               header="X-Shopify-Access-Token")
    api_key_connector.set_pagination("offset", page_size=50, start_at=0)
    api_key_connector.add_transformation("id", "product_id")
    api_key_connector.add_transformation("title", "product_name")
    api_key_connector.add_transformation("vendor", "supplier")

    print("\nExample 3: REST API with API Key")
    api_key_connector.print_config()

    # Print summaries
    print(f"\n{'='*60}")
    print("CONNECTOR SUMMARIES")
    print(f"{'='*60}")
    for connector in [rest_connector, graphql_connector, api_key_connector]:
        summary = connector.get_summary()
        print(f"\n{connector.name}:")
        for key, value in summary.items():
            print(f"  {key}: {value}")


