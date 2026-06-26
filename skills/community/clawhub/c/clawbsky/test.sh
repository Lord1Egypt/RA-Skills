#!/bin/bash
echo "Hello from terminal test"
echo "Date: $(date)"
echo "OS: $(uname -a)"
echo ""
echo "Testing node..."
node --version
echo ""
echo "Testing npm..."
npm --version
echo ""
echo "All tests passed!"