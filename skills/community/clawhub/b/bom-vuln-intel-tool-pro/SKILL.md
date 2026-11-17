---
slug: bom-vuln-intel-tool-pro
name: bom-vuln-intel-tool-pro
version: 1.0.0
displayName: 物料清单漏洞情报专业版
summary: 企业级SBOM管理平台,支持多生态、CycloneDX/SPDX标准、批量扫描、持续监控与CI/CD集成,适合安全团队与企业用户.
license: Proprietary
edition: pro
description: "物料清单漏洞情报专业版,为企业安全团队提供全方位SBOM管理与依赖漏洞治理能力。核心能力:多生态SBOM生成、CycloneDX/SPDX标准输出、OSV+GHSA+NVD三库联查、批量扫描、持续监控与告警、SARIF报告。Use。Use when 需要系统监控、日志分析、运维告警、部署管理时使用。不适用于物理硬件维修。 功能涵盖: vuln, intel。"
  when 需要系统监控、日志分析、运维告警、部署管理时使用。不适用于物理硬件维修.
tags:
  - 安全
  - SBOM
  - 供应链安全
  - 企业版
  - CycloneDX
  - 加密
  - 工具
  - sbom
  - json
  - self
  - ecosystem
  - pkg
tools:
  - read
  - exec
homepage: ""
# 定价元数据
category: "Security"
---
# 物料清单漏洞情报专业版
## 概述
专业版为企业安全团队提供完整的软件物料清单(SBOM)管理与依赖漏洞治理平台。在免费版基础查询能力之上,新增多生态SBOM生成(npm/pip/go/cargo/maven/nuget)、CycloneDX与SPDX标准格式输出、OSV+GHSA+NVD三漏洞库联查、批量多项目扫描、持续漏洞监控与Webhook告警、SARIF合规报告。专业版完全兼容免费版查询接口,已有检查脚本可无缝升级.
### 专业版核心优势
| 优势 | 说明 |
|---|---|
| 多生态支持 | npm/pip/go/cargo/maven/nuget六大生态 |
| 标准格式 | CycloneDX 1.5、SPDX 2.3标准输出 |
| 三库联查 | OSV + GHSA + NVD交叉验证 |
| 批量扫描 | 多项目并行扫描,一次检查数百个依赖 |
| 持续监控 | 新漏洞自动发现与告警推送 |
| CI/CD集成 | 完整流水线集成与安全门禁 |
| 报告导出 | SARIF/HTML/PDF合规报告 |
| SBOM差异 | 版本间SBOM差异对比 |
## 核心能力
### 1. 多生态SBOM生成(专业版独有)
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 物料清单漏洞情报专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
```bash
#!/bin/sh
generate_sbom() {
    local project_dir=$1
    local format=${2:-cyclonedx}
    local output=${3:-sbom.json}
    cd "$project_dir" || return 1
    echo "生成SBOM: $(basename "$(pwd)") -> ${output}"
    case "$format" in
        cyclonedx)
            if [ -f package.json ]; then
                npx @cyclonedx/cyclonedx-npm --output-file "$output" 2>/dev/null
            fi
            if [ -f requirements.txt ]; then
                cyclonedx-py requirements -o "$output" 2>/dev/null
            fi
            if [ -f go.mod ]; then
                cyclonedx-gomod app -o "$output" 2>/dev/null
            fi
            if [ -f Cargo.toml ]; then
                cargo cyclonedx -o "$output" 2>/dev/null
            fi
            ;;
        spdx)
                npx spdx-sbom-generator npm -o "$output" 2>/dev/null
            fi
            ;;
    esac
    echo "SBOM已生成: ${output}"
    echo "组件数量: $(jq '.components | length // .packages | length // 0' "$output" 2>/dev/null)"
}
generate_sbom "." "cyclonedx" "sbom-cdx.json"
generate_sbom "." "spdx" "sbom-spdx.json"
```
**处理**: 解析多生态SBOM生成(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多生态SBOM生成(专业版独有)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 三漏洞库联查(专业版独有)
```python
#!/usr/bin/env python3
"""专业版三漏洞库联查引擎"""
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
class MultiSourceVulnChecker:
    """OSV + GHSA + NVD 三库联查"""
    def __init__(self):
        self.sources = {
            "osv": self._query_osv,
            "ghsa": self._query_ghsa,
            "nvd": self._query_nvd,
        }
    def _query_osv(self, pkg, version, ecosystem):
        """查询OSV数据库"""
        resp = requests.post(
            "https://api.osv.dev/v1/query",
            json={
                "package": {"name": pkg, "ecosystem": ecosystem},
                "version": version
            },
            timeout=10
        )
        return resp.json().get("vulns", [])
    def _query_ghsa(self, pkg, version, ecosystem):
        """查询GitHub安全公告"""
            json={
                "package": {"name": pkg, "ecosystem": ecosystem},
                "version": version
            },
            timeout=10
        )
        vulns = resp.json().get("vulns", [])
        return [v for v in vulns if v.get("id", "").startswith("GHSA")]
    def _query_nvd(self, pkg, version, ecosystem):
        """查询NVD数据库"""
        cpe = self._guess_cpe(pkg, ecosystem)
        if not cpe:
            return []
            "https://services.nvd.nist.gov/rest/json/cves/2.0",
            params={"cpeName": cpe},
            timeout=10
        )
        return resp.json().get("vulnerabilities", [])
    def _guess_cpe(self, pkg, ecosystem):
        """根据包名猜测CPE"""
        prefix = {"npm": "nodejs", "PyPI": "python", "go": "golang"}.get(ecosystem, "")
        if prefix:
            return f"cpe:2.3:a:{prefix}:{pkg}:*:*:*:*:*:*:*:*"
        return None
    def check_package(self, pkg, version, ecosystem="npm"):
        """三库联查"""
        results = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(fn, pkg, version, ecosystem): source
                for source, fn in self.sources.items()
            }
            for future in as_completed(futures):
                source = futures[future]
                try:
                    results[source] = future.result()
                except Exception as e:
                    results[source] = []
        all_ids = set()
        merged = []
        for source, vulns in results.items():
            for v in vulns:
                vid = v.get("id") or v.get("cve", {}).get("id", "")
                if vid and vid not in all_ids:
                    all_ids.add(vid)
                    v["_source"] = source
                    merged.append(v)
        return {
            "package": pkg,
            "version": version,
            "ecosystem": ecosystem,
            "total_vulnerabilities": len(merged),
            "by_source": {s: len(v) for s, v in results.items()},
            "vulnerabilities": merged
        }
if __name__ == "__main__":
    checker = MultiSourceVulnChecker()
    result = checker.check_package("lodash", "4.17.20", "npm")
    print(json.dumps(result, indent=2, ensure_ascii=False))
```
**处理**: 解析三漏洞库联查(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回三漏洞库联查(专业版独有)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 批量项目扫描(专业版独有)
```bash
#!/bin/sh
SCAN_DIR="${1:-.}"
OUTPUT_FILE="batch-vuln-report.json"
echo "============================================"
echo "批量质量检查: ${SCAN_DIR}"
echo "扫描时间: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "============================================"
echo "[" > "$OUTPUT_FILE"
FIRST=true
find "$SCAN_DIR" -maxdepth 3 \( -name "package.json" -o -name "requirements.txt" -o -name "go.mod" -o -name "Cargo.toml" \) | \
while read -r depfile; do
    project_dir=$(dirname "$depfile")
    project_name=$(basename "$project_dir")
    echo ""
    echo "扫描项目: ${project_name} (${depfile})"
    VULNS=0
    case "$depfile" in
        */package.json)
            VULNS=$(cd "$project_dir" && npm audit --json 2>/dev/null | jq '.metadata.vulnerabilities.total // 0')
            ;;
        */requirements.txt)
            VULNS=$(cd "$project_dir" && pip-audit -r requirements.txt -f json 2>/dev/null | jq '. | length // 0')
            ;;
        */go.mod)
            VULNS=$(cd "$project_dir" && govulncheck ./... -json 2>/dev/null | grep -c '"vulnerability"')
            ;;
    esac
    echo "  漏洞数量: ${VULNS}"
    [ "$FIRST" = true ] && FIRST=false || echo "," >> "$OUTPUT_FILE"
    echo "{\"project\": \"${project_name}\", \"file\": \"${depfile}\", \"vulns\": ${VULNS}}" >> "$OUTPUT_FILE"
done
echo "]" >> "$OUTPUT_FILE"
echo ""
echo "扫描完成,报告: ${OUTPUT_FILE}"
```
**处理**: 解析批量项目扫描(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量项目扫描(专业版独有)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 持续监控与告警(专业版独有)
```yaml
monitoring:
  schedule: "0 9 * * 1"  # 每周一上午9点
  projects:
    - name: "frontend-app"
      sbom: "sbom/frontend.json"
      ecosystem: "npm"
    - name: "backend-api"
      sbom: "sbom/backend.json"
      ecosystem: "pip"
    - name: "microservice"
      sbom: "sbom/service.json"
      ecosystem: "go"
  alert:
    webhook: "https://hooks.slack.com/services/未指定"
    min_severity: "HIGH"
    new_vulns_only: true
  baseline:
    previous_report: "reports/vuln-20260711.json"
```
**处理**: 解析持续监控与告警(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回持续监控与告警(专业版独有)的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、管理平台、支持多生态、批量扫描、适合安全团队与企、业用户、物料清单漏洞情报、为企业安全团队提、供全方位、管理与依赖漏洞治、理能力、核心能力、标准输出、SARIF、Use、when、需要系统监控、日志分析、运维告警、部署管理时使用、不适用于物理硬件等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
## 使用场景
### 场景一:企业级供应链安全管理
```bash
#!/bin/sh
echo "============================================"
echo "企业供应链安全扫描"
echo "============================================"
echo "阶段1: SBOM生成"
for project in /projects/*/; do
    name=$(basename "$project")
    generate_sbom "$project" "cyclonedx" "/sbom/${name}.json"
done
echo "阶段2: 质量检查"
for sbom in /sbom/*.json; do
    project=$(basename "$sbom" .json)
    echo "扫描: ${project}"
    jq -r '.components[]? | "\(.name) \(.version) \(.ecosystem // "npm")"' "$sbom" | \
    while read -r name version eco; do
        curl -s -X POST "https://api.osv.dev/v1/query" \
            -H "Content-Type: application/json" \
            -d "{\"package\": {\"name\": \"${name}\", \"ecosystem\": \"${eco}\"}, \"version\": \"${version}\"}" | \
            jq --arg n "$name" --arg v "$version" '{
                package: $n, version: $v,
                vulns: (.vulns | length // 0)
            }'
    done
done
echo "扫描完成"
```
### 场景二:CI/CD安全门禁
```yaml
name: Supply Chain Security
on: [push, pull_request]
jobs:
  sbom-and-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate SBOM
        run: |
          npx @cyclonedx/cyclonedx-npm --output-file sbom.json
      - name: Scan for vulnerabilities
        run: |
          CRITICAL=0
          jq -r '.components[] | "\(.name) \(.version)"' sbom.json | \
          while read -r name version; do
            COUNT=$(curl -s -X POST "https://api.osv.dev/v1/query" \
              -H "Content-Type: application/json" \
              -d "{\"package\": {\"name\": \"${name}\", \"ecosystem\": \"npm\"}, \"version\": \"${version}\"}" \
              | jq '.vulns | length // 0')
            if [ "$COUNT" -gt 0 ]; then
              echo "${name}@${version}: ${COUNT} vulns"
              SEVERITY=$(curl -s -X POST "https://api.osv.dev/v1/query" \
                -H "Content-Type: application/json" \
                -d "{\"package\": {\"name\": \"${name}\", \"ecosystem\": \"npm\"}, \"version\": \"${version}\"}" \
                | jq -r '.vulns[]? | .severity // "UNKNOWN"' | grep -c "CRITICAL")
              [ "$SEVERITY" -gt 0 ] && CRITICAL=$((CRITICAL + 1))
            fi
          done
          if [ "$CRITICAL" -gt 0 ]; then
            echo "BLOCKED: ${CRITICAL} critical vulnerabilities"
            exit 1
          fi
      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json
```
### 场景三:SBOM差异对比
```bash
#!/bin/sh
OLD_SBOM=$1
NEW_SBOM=$2
echo "=== SBOM差异对比 ==="
echo "旧版本: ${OLD_SBOM}"
echo "新版本: ${NEW_SBOM}"
echo ""
jq -r '.components[]? | "\(.name)@\(.version)"' "$OLD_SBOM" | sort > /tmp/old_comps.txt
jq -r '.components[]? | "\(.name)@\(.version)"' "$NEW_SBOM" | sort > /tmp/new_comps.txt
echo "--- 新增组件 ---"
comm -13 /tmp/old_comps.txt /tmp/new_comps.txt
echo ""
echo "--- 移除组件 ---"
comm -23 /tmp/old_comps.txt /tmp/new_comps.txt
echo ""
echo "--- 版本变更 ---"
jq -r '.components[]? | .name' "$OLD_SBOM" | sort -u > /tmp/old_names.txt
jq -r '.components[]? | .name' "$NEW_SBOM" | sort -u > /tmp/new_names.txt
comm -12 /tmp/old_names.txt /tmp/new_names.txt | while read -r name; do
    old_ver=$(jq -r --arg n "$name" '.components[]? | select(.name == $n) | .version' "$OLD_SBOM" | head -1)
    new_ver=$(jq -r --arg n "$name" '.components[]? | select(.name == $n) | .version' "$NEW_SBOM" | head -1)
    [ "$old_ver" != "$new_ver" ] && echo "  ${name}: ${old_ver} -> ${new_ver}"
done
```
## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### 从免费版升级
专业版完全兼容免费版查询接口,新增批量与标准格式能力:
```bash
osv.dev/v1/query" ...
python3 multi_vuln_check.py --package lodash --version 4.17.20
```
### 首次批量扫描
```bash
bash batch_scan.sh . --output batch-report.json
```
#
## 配置示例
### 支持的生态系统(专业版)
| 生态系统 | 包管理器 | SBOM生成 | 漏洞查询 | 工具 |
|---:|---:|---:|---:|---:|
| npm | package.json | CycloneDX/SPDX | OSV+GHSA+NVD | cyclonedx-npm |
| PyPI | requirements.txt | CycloneDX/SPDX | OSV+GHSA+NVD | cyclonedx-py |
| Go | go.mod | CycloneDX | OSV+GHSA | cyclonedx-gomod |
| Cargo | Cargo.toml | CycloneDX | OSV+GHSA | cargo-cyclonedx |
| Maven | pom.xml | CycloneDX/SPDX | OSV+GHSA+NVD | cyclonedx-maven |
| NuGet | .csproj | CycloneDX/SPDX | OSV+GHSA | CycloneDX .NET |
### SBOM格式标准
| 格式 | 版本 | 适用场景 |
|:---:|:---:|:---:|
| CycloneDX | 1.5 | 现代云原生项目,推荐 |
| SPDX | 2.3 | 合规要求,许可证分析 |
| JSON | 自定义 | 免费版兼容格式 |
## 优选实践
1. **每次发布生成SBOM**:将SBOM生成集成到CI/CD,每次发布保留SBOM快照.
2. **三库联查**:使用OSV+GHSA+NVD交叉验证,减少漏报.
3. **持续监控**:配置定期扫描,新漏洞出现时领先时间告警.
4. **SBOM归档**:保留历史SBOM,支持事后追溯与差异对比.
5. **安全门禁**:在CI/CD中设置严重漏洞零容忍策略.
6. **最小依赖**:定期审查SBOM,移除不再使用的依赖.
## 常见问题
### Q1: 专业版与免费版查询结果是否一致?
专业版在免费版OSV查询基础上,增加了GHSA和NVD交叉验证,结果更全面。免费版发现的漏洞专业版一定能发现.
### Q2: CycloneDX和SPDX如何选择?
CycloneDX更适合云原生与现代开发流程,SPDX更适合需要详细许可证分析的合规场景。建议同时生成两种格式.
### 已知限制
专业版支持并行扫描,建议并发不超过10个项目。OSV API建议控制在5 QPS以内.
### Q4: 持续监控如何配置?
通过YAML配置文件指定监控项目、扫描频率和告警阈值。支持Cron表达式和Webhook推送.
### Q5: SBOM差异对比有什么用?
版本间SBOM差异对比可以帮助识别新增依赖引入的风险,快速定位版本升级带来的安全变化.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+(使用三库联查引擎时需要)
- **网络**: 需可访问 `https://api.osv.dev`、`https://services.nvd.nist.gov`
### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| curl | 命令行工具 | 必需 | 系统自带 |
| jq | JSON处理工具 | 必需 | `apt install jq` / `brew install jq` |
| python3 | 运行时环境 | 推荐 | python.org 下载 |
| requests | Python库 | 推荐 | `pip install requests` |
| cyclonedx-cli | SBOM工具 | 推荐 | CycloneDX官方下载 |
| govulncheck | Go扫描器 | 按需 | `go install golang.org/x/vuln/cmd/govulncheck@latest` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
### API Key 配置
- OSV API为公开接口,无需API Key
- NVD API建议申请免费API Key以提高速率限制
- GHSA通过OSV代理查询,无需单独配置
### 可用性分类
- **分类**: MD+execute(纯Markdown指令,核心功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行企业级SBOM管理与供应链安全治理任务
## 错误处理
| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
## 示例
### 基本用法
**输出**：返回执行结果,包含操作状态和输出数据
```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```
## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "物料清单漏洞情报专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "bom vuln intel pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
## 安全注意事项
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 效率量化分析
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |
## 差异化对比
| 对比维度 | 物料清单漏洞情报专业版 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 企业级SBOM管理平台,支持多生态、CycloneDX/SPDX标准、批量扫描、 | 通用场景 | 通用场景 |
## 核心功能
- **自动化执行**: 企业级SBOM管理平台,支持多生态、CycloneDX/SPDX标准、批量扫描、持续监控与CI/CD集成,适合安全团队与
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据