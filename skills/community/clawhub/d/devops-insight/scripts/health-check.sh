#!/bin/bash

# DevOps Insight MCP Server Health Check Script

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "DevOps Insight MCP Server Health Check"
echo "================================"

# Check function
check_service() {
    local service_name=$1
    local check_command=$2

    echo -n "Checking $service_name... "
    if eval "$check_command" &> /dev/null; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed${NC}"
        return 1
    fi
}

# Check Kubernetes
check_service "Kubernetes" "kubectl cluster-info"

# Check PostgreSQL
check_service "PostgreSQL" "pg_isready -h localhost -p 5432"

# Check Redis
check_service "Redis" "redis-cli ping"

# Check Elasticsearch
check_service "Elasticsearch" "curl -s http://localhost:9200/_cluster/health"

# Check Neo4j
check_service "Neo4j" "curl -s http://localhost:7474"

# Check GitHub CLI
check_service "GitHub CLI" "gh auth status"

echo ""
echo "================================"
echo "Health check complete"
