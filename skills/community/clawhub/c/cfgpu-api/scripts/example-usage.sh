#!/bin/bash
# CFGPU API Usage Examples

# Set your API token
export CFGPU_API_TOKEN="YOUR_API_TOKEN"

# Make scripts executable
chmod +x cfgpu-helper.sh

echo "=== Example 1: List Available Resources ==="
echo ""
echo "1. List regions:"
./cfgpu-helper.sh list-regions

echo ""
echo "2. List GPU types:"
./cfgpu-helper.sh list-gpus

echo ""
echo "3. List system images:"
./cfgpu-helper.sh list-system-images VM

echo ""
echo "=== Example 2: Create and Manage Instance ==="
echo ""
echo "Note: Uncomment and modify the following commands to use"

# Example: Create an instance
# INSTANCE_ID=$(./cfgpu-helper.sh create hz qnid2x6c 1 image_exc6f72b 1 Day "Test-Instance" | jq -r '.content.instanceId')
# echo "Created instance: $INSTANCE_ID"

# Example: Check instance status
# ./cfgpu-helper.sh status "$INSTANCE_ID"

# Example: Start instance
# ./cfgpu-helper.sh start "$INSTANCE_ID"

# Example: Stop instance
# ./cfgpu-helper.sh stop "$INSTANCE_ID"

# Example: Release instance
# ./cfgpu-helper.sh release "$INSTANCE_ID"

echo ""
echo "=== Example 3: Interactive Creation ==="
echo ""
echo "Run interactive wizard:"
echo "./cfgpu-helper.sh quick-create"

echo ""
echo "=== Example 4: Query Instances ==="
echo ""
echo "Query all instances:"
echo "./cfgpu-helper.sh query"

echo ""
echo "Query running instances:"
echo "./cfgpu-helper.sh query \"\" \"RUNNING\""

echo ""
echo "=== Example 5: Batch Operations ==="
echo ""
cat << 'EOF'
# List all instances and stop them
INSTANCES=$(./cfgpu-helper.sh all-status | jq -r '.[].instanceId')
for INSTANCE in $INSTANCES; do
    echo "Stopping instance: $INSTANCE"
    ./cfgpu-helper.sh stop "$INSTANCE"
done

# List all stopped instances and release them
STOPPED_INSTANCES=$(./cfgpu-helper.sh query "" "CLOSED" | jq -r '.records[].instanceId')
for INSTANCE in $STOPPED_INSTANCES; do
    echo "Releasing instance: $INSTANCE"
    ./cfgpu-helper.sh release "$INSTANCE"
done
EOF

echo ""
echo "=== Tips ==="
echo "1. Set API token: export CFGPU_API_TOKEN='your-token'"
echo "2. Or create token file: echo 'your-token' > ~/.cfgpu/token && chmod 600 ~/.cfgpu/token"
echo "3. Install jq for JSON parsing: apt-get install jq or brew install jq"
echo "4. Check instance status regularly to avoid unexpected charges"
echo "5. Always stop instances when not in use"
echo "6. Release instances you no longer need"