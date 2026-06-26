#!/usr/bin/env bash
#
# csharp-lsp 원타임 셋업 스크립트
# 멱등성 보장 — 몇 번이든 재실행해도 안전합니다.
#
# 수행 항목:
#   1. .NET SDK 존재 확인 (없으면 안내 후 종료)
#   2. csharp-ls 설치 (이미 있으면 스킵)
#   3. ~/.dotnet/tools PATH 등록 (이미 있으면 스킵)
#   4. lsp-query 심볼릭 링크 생성 (이미 있으면 스킵)
#   5. puppeteer 캐시 디렉토리 생성 (데몬용)
#   6. 동작 검증 (선택)
#
# 사용법:
#   bash setup.sh
#   bash setup.sh --verify    # 셋업 후 간단한 동작 테스트까지 수행
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LSP_QUERY="$SCRIPT_DIR/lsp-query.py"
CSHARP_LS_VERSION="0.20.0"
DOTNET_TOOLS="$HOME/.dotnet/tools"
SYMLINK_PATH="/usr/local/bin/lsp-query"
CACHE_DIR="$HOME/.cache/lsp-query"

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
skip() { echo -e "  ${YELLOW}→${NC} $1 (이미 완료)"; }
fail() { echo -e "  ${RED}✗${NC} $1"; }
info() { echo -e "  $1"; }

echo ""
echo "═══════════════════════════════════════════"
echo "  csharp-lsp 셋업"
echo "═══════════════════════════════════════════"
echo ""

# ─────────────────────────────────────────────
# 1. .NET SDK 확인
# ─────────────────────────────────────────────
echo "[1/5] .NET SDK 확인"

if command -v dotnet &>/dev/null; then
    DOTNET_VER=$(dotnet --version 2>/dev/null || echo "unknown")
    ok ".NET SDK $DOTNET_VER"
else
    fail ".NET SDK가 설치되어 있지 않습니다."
    info ""
    info "설치 방법:"
    info "  Ubuntu/Debian:  sudo apt install dotnet-sdk-9.0"
    info "  macOS:          brew install dotnet-sdk"
    info "  기타:           https://dot.net/download"
    info ""
    exit 1
fi

# ─────────────────────────────────────────────
# 2. csharp-ls 설치
# ─────────────────────────────────────────────
echo "[2/5] csharp-ls 설치"

# PATH에 dotnet tools가 있는지 먼저 확인 (which가 찾을 수 있도록)
export PATH="$DOTNET_TOOLS:$PATH"

if command -v csharp-ls &>/dev/null; then
    CS_VER=$(csharp-ls --version 2>/dev/null || echo "installed")
    skip "csharp-ls $CS_VER"
else
    info "csharp-ls $CSHARP_LS_VERSION 설치 중..."
    if dotnet tool install --global csharp-ls --version "$CSHARP_LS_VERSION" 2>/dev/null; then
        ok "csharp-ls $CSHARP_LS_VERSION 설치 완료"
    elif dotnet tool list --global 2>/dev/null | grep -q csharp-ls; then
        # 다른 버전이 이미 있을 수 있음
        skip "csharp-ls (다른 버전이 이미 설치됨)"
    else
        fail "csharp-ls 설치 실패"
        info "수동 설치: dotnet tool install --global csharp-ls"
        exit 1
    fi
fi

# ─────────────────────────────────────────────
# 3. PATH 등록 (~/.dotnet/tools)
# ─────────────────────────────────────────────
echo "[3/5] PATH 등록"

path_registered=false

for rcfile in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rcfile" ]; then
        if grep -q '\.dotnet/tools' "$rcfile" 2>/dev/null; then
            skip "$rcfile 에 이미 등록됨"
            path_registered=true
        else
            echo 'export PATH="$HOME/.dotnet/tools:$PATH"' >> "$rcfile"
            ok "$rcfile 에 PATH 추가"
            path_registered=true
        fi
    fi
done

if [ "$path_registered" = false ]; then
    fail "shell RC 파일을 찾을 수 없습니다 (.bashrc 또는 .zshrc)"
    info "수동으로 추가: export PATH=\"\$HOME/.dotnet/tools:\$PATH\""
fi

# ─────────────────────────────────────────────
# 4. lsp-query 심볼릭 링크
# ─────────────────────────────────────────────
echo "[4/5] lsp-query 심볼릭 링크"

if [ ! -f "$LSP_QUERY" ]; then
    fail "lsp-query.py를 찾을 수 없습니다: $LSP_QUERY"
    exit 1
fi

chmod +x "$LSP_QUERY" 2>/dev/null || true

if [ -L "$SYMLINK_PATH" ] && [ "$(readlink -f "$SYMLINK_PATH")" = "$(readlink -f "$LSP_QUERY")" ]; then
    skip "$SYMLINK_PATH → $LSP_QUERY"
elif [ -w "$(dirname "$SYMLINK_PATH")" ] 2>/dev/null; then
    ln -sf "$LSP_QUERY" "$SYMLINK_PATH"
    ok "$SYMLINK_PATH → $LSP_QUERY"
else
    # sudo 필요
    if command -v sudo &>/dev/null; then
        info "심볼릭 링크 생성에 sudo가 필요합니다..."
        if [ -n "${SUDO_PASS:-}" ]; then
            echo "$SUDO_PASS" | sudo -S ln -sf "$LSP_QUERY" "$SYMLINK_PATH" 2>/dev/null
            ok "$SYMLINK_PATH → $LSP_QUERY (sudo)"
        elif sudo -n true 2>/dev/null; then
            sudo ln -sf "$LSP_QUERY" "$SYMLINK_PATH"
            ok "$SYMLINK_PATH → $LSP_QUERY (sudo)"
        else
            fail "sudo 권한 없이 $SYMLINK_PATH 에 링크를 만들 수 없습니다."
            info "수동 실행: sudo ln -sf $LSP_QUERY $SYMLINK_PATH"
            info "또는 다른 경로에 링크: ln -sf $LSP_QUERY ~/.local/bin/lsp-query"
        fi
    else
        fail "$SYMLINK_PATH 에 쓰기 권한이 없습니다."
        info "수동 실행: sudo ln -sf $LSP_QUERY $SYMLINK_PATH"
    fi
fi

# ─────────────────────────────────────────────
# 5. 캐시 디렉토리
# ─────────────────────────────────────────────
echo "[5/5] 캐시 디렉토리"

if [ -d "$CACHE_DIR" ]; then
    skip "$CACHE_DIR 존재"
else
    mkdir -p "$CACHE_DIR"
    ok "$CACHE_DIR 생성"
fi

echo ""
echo "═══════════════════════════════════════════"
echo -e "  ${GREEN}셋업 완료!${NC}"
echo "═══════════════════════════════════════════"
echo ""
echo "  사용법:"
echo "    LSP_WORKSPACE=/path/to/solution lsp-query hover file.cs 5 16"
echo "    LSP_WORKSPACE=/path/to/solution lsp-query references file.cs 10 20"
echo "    lsp-query servers    # 실행 중인 서버 확인"
echo "    lsp-query shutdown   # 데몬 종료"
echo ""

# ─────────────────────────────────────────────
# 검증 (--verify 옵션)
# ─────────────────────────────────────────────
if [[ "${1:-}" == "--verify" ]]; then
    echo "═══════════════════════════════════════════"
    echo "  동작 검증"
    echo "═══════════════════════════════════════════"
    echo ""

    TEST_DIR=$(mktemp -d /tmp/csharp-lsp-test.XXXXXX)
    trap "rm -rf $TEST_DIR" EXIT

    # 미니 C# 프로젝트 생성
    info "테스트 프로젝트 생성 중..."
    mkdir -p "$TEST_DIR/Verify"

    cat > "$TEST_DIR/Verify/Verify.csproj" << 'PROJEOF'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net9.0</TargetFramework>
  </PropertyGroup>
</Project>
PROJEOF

    cat > "$TEST_DIR/Verify/Program.cs" << 'CSEOF'
namespace Verify;
public class Calculator
{
    public int Add(int a, int b) => a + b;
}
public class Program
{
    static void Main()
    {
        var calc = new Calculator();
        System.Console.WriteLine(calc.Add(1, 2));
    }
}
CSEOF

    dotnet restore "$TEST_DIR/Verify" -q 2>/dev/null || true

    info "LSP 쿼리 테스트 (첫 실행은 30초+ 소요)..."
    lsp-query shutdown 2>/dev/null || true
    rm -f "$CACHE_DIR/daemon.sock" "$CACHE_DIR/daemon.sock.pid"

    RESULT=$(LSP_WORKSPACE="$TEST_DIR/Verify" lsp-query hover "$TEST_DIR/Verify/Program.cs" 4 16 2>&1)

    if echo "$RESULT" | grep -q "Calculator.Add"; then
        ok "hover 테스트 통과: $RESULT"
        echo ""
        echo -e "  ${GREEN}모든 검증 완료!${NC}"
    else
        fail "hover 테스트 실패"
        info "결과: $RESULT"
        info "lsp-query shutdown 후 재시도해보세요."
    fi

    lsp-query shutdown 2>/dev/null || true
    echo ""
fi
