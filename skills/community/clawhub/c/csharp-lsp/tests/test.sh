#!/usr/bin/env bash
#
# csharp-lsp integration test suite
# Runs in a clean Docker container to verify install + functionality.
#
# Usage:
#   bash tests/test.sh              # from repo root
#   bash tests/test.sh --no-build   # skip Docker image build
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="csharp-lsp-test"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

pass() { echo -e "  ${GREEN}✓${NC} $1"; PASSED=$((PASSED+1)); }
fail() { echo -e "  ${RED}✗${NC} $1"; FAILED=$((FAILED+1)); }

PASSED=0
FAILED=0

# ─────────────────────────────────────────────
# Build Docker image
# ─────────────────────────────────────────────
if [[ "${1:-}" != "--no-build" ]]; then
    echo "Building test image..."
    docker build -t "$IMAGE_NAME" -f "$SCRIPT_DIR/Dockerfile" "$SCRIPT_DIR" -q > /dev/null
    echo ""
fi

# ─────────────────────────────────────────────
# Run tests inside container
# ─────────────────────────────────────────────
echo "═══════════════════════════════════════════"
echo "  csharp-lsp test suite"
echo "═══════════════════════════════════════════"
echo ""

TEST_OUTPUT=$(docker run --rm \
    -v "$REPO_DIR:/skill/csharp-lsp:ro" \
    "$IMAGE_NAME" \
    bash -c '
        export PATH="$HOME/.dotnet/tools:$PATH"

        # Copy to writable location
        cp -r /skill/csharp-lsp /tmp/csharp-lsp
        chmod +x /tmp/csharp-lsp/scripts/*.sh /tmp/csharp-lsp/scripts/*.py

        # ═══ TEST 1: Setup ═══
        echo "TEST:setup:START"
        bash /tmp/csharp-lsp/scripts/setup.sh 2>&1
        if command -v csharp-ls &>/dev/null && [ -L /usr/local/bin/lsp-query ]; then
            echo "TEST:setup:PASS"
        else
            echo "TEST:setup:FAIL"
        fi

        # ═══ TEST 2: Idempotency ═══
        echo "TEST:idempotency:START"
        OUTPUT=$(bash /tmp/csharp-lsp/scripts/setup.sh 2>&1)
        # All steps should say "이미 완료" or similar skip message
        if echo "$OUTPUT" | grep -q "이미 완료"; then
            echo "TEST:idempotency:PASS"
        else
            echo "TEST:idempotency:FAIL"
        fi

        # ═══ Create test project ═══
        mkdir -p /tmp/test/Mini
        cat > /tmp/test/Mini/Mini.csproj << PROJ
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net9.0</TargetFramework>
  </PropertyGroup>
</Project>
PROJ
        cat > /tmp/test/Mini/Program.cs << CS
namespace Mini;

public class Calculator
{
    public int Add(int a, int b) => a + b;
    public int Multiply(int a, int b) => a * b;
}

public class Program
{
    static void Main()
    {
        var calc = new Calculator();
        System.Console.WriteLine(calc.Add(1, 2));
    }
}
CS
        dotnet restore /tmp/test/Mini -q 2>&1

        export LSP_WORKSPACE=/tmp/test/Mini
        lsp-query shutdown 2>/dev/null || true
        rm -f ~/.cache/lsp-query/daemon.sock ~/.cache/lsp-query/daemon.sock.pid

        # ═══ TEST 3: Hover ═══
        echo "TEST:hover:START"
        RESULT=$(timeout 120 lsp-query hover /tmp/test/Mini/Program.cs 5 16 2>&1)
        if echo "$RESULT" | grep -q "Calculator.Add"; then
            echo "TEST:hover:PASS"
        else
            echo "TEST:hover:FAIL:$RESULT"
        fi

        # ═══ TEST 4: Symbols ═══
        echo "TEST:symbols:START"
        RESULT=$(timeout 30 lsp-query symbols /tmp/test/Mini/Program.cs 2>&1)
        if echo "$RESULT" | grep -q "Calculator" && echo "$RESULT" | grep -q "Program"; then
            echo "TEST:symbols:PASS"
        else
            echo "TEST:symbols:FAIL:$RESULT"
        fi

        # ═══ TEST 5: Definition ═══
        echo "TEST:definition:START"
        RESULT=$(timeout 30 lsp-query definition /tmp/test/Mini/Program.cs 14 35 2>&1)
        if echo "$RESULT" | grep -q "Program.cs"; then
            echo "TEST:definition:PASS"
        else
            echo "TEST:definition:FAIL:$RESULT"
        fi

        # ═══ TEST 6: References ═══
        echo "TEST:references:START"
        RESULT=$(timeout 30 lsp-query references /tmp/test/Mini/Program.cs 5 16 2>&1)
        if echo "$RESULT" | grep -q "Program.cs"; then
            echo "TEST:references:PASS"
        else
            echo "TEST:references:FAIL:$RESULT"
        fi

        lsp-query shutdown 2>/dev/null || true
    ' 2>&1)

# ─────────────────────────────────────────────
# Parse results
# ─────────────────────────────────────────────
echo "Tests:"

for test_name in setup idempotency hover symbols definition references; do
    if echo "$TEST_OUTPUT" | grep -q "TEST:${test_name}:PASS"; then
        pass "$test_name"
    else
        fail "$test_name"
        # Show failure detail if available
        DETAIL=$(echo "$TEST_OUTPUT" | grep "TEST:${test_name}:FAIL" | sed "s/TEST:${test_name}:FAIL://")
        if [ -n "$DETAIL" ]; then
            echo "       $DETAIL"
        fi
    fi
done

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════"
TOTAL=$((PASSED + FAILED))
if [ "$FAILED" -eq 0 ]; then
    echo -e "  ${GREEN}All $TOTAL tests passed!${NC}"
else
    echo -e "  ${RED}$FAILED/$TOTAL tests failed${NC}"
fi
echo "═══════════════════════════════════════════"

# Cleanup
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true

exit "$FAILED"
