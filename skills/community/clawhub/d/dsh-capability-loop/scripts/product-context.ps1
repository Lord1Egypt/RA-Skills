# product-context.ps1 — 扫描工程，产出「产品/设计上下文」骨架（只读）
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File .\product-context.ps1 -Project <工程根> [-OutFile <md>]
# 退出码：0 = 完成；2 = 参数/路径错误
# 注意：自动扫描只给「线索」，设计/业务判断仍需人工核对（见 references/55-design-intake.md）。
[CmdletBinding()]
param(
    [string]$Project = '',
    [string]$OutFile = '',
    [int]$MaxFiles = 8000
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version 2.0

if (-not $Project) { $Project = (Get-Location).Path }
if (-not (Test-Path -LiteralPath $Project -PathType Container)) {
    Write-Host ('[FAIL] 工程目录不存在：' + $Project) -ForegroundColor Red
    exit 2
}
$Project = (Resolve-Path -LiteralPath $Project).Path
if (-not $OutFile) {
    $tmpDir = Join-Path (Get-Location).Path '.tmp\capability-loop'
    try {
        if (-not (Test-Path -LiteralPath $tmpDir)) { New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null }
    } catch { }
    $OutFile = Join-Path $tmpDir 'product-context.md'
}

function Read-Utf8 {
    param([string]$Path)
    try { return [System.IO.File]::ReadAllText($Path, (New-Object System.Text.UTF8Encoding($false))) } catch { return '' }
}
function Get-Deps {
    param([string]$PkgPath)
    $names = New-Object System.Collections.ArrayList
    $txt = Read-Utf8 $PkgPath
    if ($txt -eq '') { return $names }
    try {
        $j = $txt | ConvertFrom-Json
        foreach ($sec in @('dependencies', 'devDependencies', 'peerDependencies')) {
            $obj = $j.PSObject.Properties[$sec]
            if ($obj -and $obj.Value) {
                foreach ($p in $obj.Value.PSObject.Properties) { [void]$names.Add($p.Name) }
            }
        }
    } catch { }
    return $names
}

# 1) 收集 package.json（根 + apps/packages 一层）
$pkgFiles = New-Object System.Collections.ArrayList
$rootPkg = Join-Path $Project 'package.json'
if (Test-Path -LiteralPath $rootPkg) { [void]$pkgFiles.Add($rootPkg) }
foreach ($sub in @('apps', 'packages')) {
    $d = Join-Path $Project $sub
    if (Test-Path -LiteralPath $d) {
        foreach ($child in @(Get-ChildItem -LiteralPath $d -Directory -ErrorAction SilentlyContinue)) {
            $p = Join-Path $child.FullName 'package.json'
            if (Test-Path -LiteralPath $p) { [void]$pkgFiles.Add($p) }
        }
    }
}
$allDeps = New-Object System.Collections.ArrayList
foreach ($pf in $pkgFiles) { foreach ($n in (Get-Deps $pf)) { [void]$allDeps.Add($n) } }
$allDeps = @($allDeps | Sort-Object -Unique)

$known = [ordered]@{
    'UI 框架/组件库' = @('ant-design-vue', 'antd', 'element-plus', 'element-ui', '@arco-design/web-vue', 'arco-design', 'naive-ui', 'vant', 'tdesign-vue-next', 'semi-ui', '@mui/material', '@chakra-ui/react', 'vuetify', 'quasar')
    '样式方案' = @('tailwindcss', 'unocss', 'sass', 'less', 'postcss', 'windicss')
    '图表' = @('echarts', 'vue-echarts', '@antv/g2', '@antv/g6', 'recharts', 'chart.js')
    '图标' = @('lucide-vue-next', 'lucide-react', '@ant-design/icons-vue', '@ant-design/icons', '@element-plus/icons-vue')
    '状态/请求' = @('pinia', 'vuex', 'zustand', 'mobx', 'axios', 'alova', '@tanstack/vue-query')
    '后台模板' = @('@vben/common-ui', '@vben/access', 'vben-admin', '@vben/vbencomponents')
}
$hits = New-Object System.Collections.ArrayList
foreach ($cat in $known.Keys) {
    $found = @($known[$cat] | Where-Object { $allDeps -contains $_ })
    if ($found.Count -gt 0) { [void]$hits.Add(@($cat, ($found -join ', '))) }
}
if ($allDeps.Count -gt 0) { [void]$hits.Add(@('依赖总数', [string]$allDeps.Count)) }

# 2) 页面/接口/样式规模（限深，避免扫 node_modules）
$srcDirs = New-Object System.Collections.ArrayList
$rootSrc = Join-Path $Project 'src'
if (Test-Path -LiteralPath $rootSrc) { [void]$srcDirs.Add($rootSrc) }
if (Test-Path -LiteralPath (Join-Path $Project 'apps')) {
    foreach ($c in @(Get-ChildItem -LiteralPath (Join-Path $Project 'apps') -Directory -ErrorAction SilentlyContinue)) {
        $s = Join-Path $c.FullName 'src'
        if (Test-Path -LiteralPath $s) { [void]$srcDirs.Add($s) }
    }
}
$files = @()
$fileBudgetHit = $false
foreach ($s in $srcDirs) {
    $got = @(Get-ChildItem -LiteralPath $s -Recurse -Depth 5 -File -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch 'node_modules|dist|\.git' })
    $files += $got
    if ($files.Count -gt $MaxFiles) { $fileBudgetHit = $true; $files = @($files | Select-Object -First $MaxFiles); break }
}
$routerFiles = @($files | Where-Object { $_.Name -match 'router|routes' -or $_.FullName -match '\\router\\' }).Count
$apiFiles = @($files | Where-Object { $_.FullName -match '\\api\\' }).Count
$viewFiles = @($files | Where-Object { $_.FullName -match '\\views?\\' }).Count
$mockFiles = @($files | Where-Object { $_.Name -match 'mock' }).Count
$styleFileList = @($files | Where-Object { $_.Extension -in @('.css', '.scss', '.less', '.sass') })
$styleFiles = $styleFileList.Count
$themeFiles = @($files | Where-Object { $_.Name -match 'token|theme|variable|var\.' -and $_.Extension -in @('.ts', '.js', '.json', '.css', '.scss', '.less', '.mjs') })
$chartTheme = @($files | Where-Object { $_.Name -match 'chart.*theme|theme.*chart' })

# 3) 文档与约定
$docFiles = @()
foreach ($d in @('docs', '.')) {
    $p = Join-Path $Project $d
    if (Test-Path -LiteralPath $p) {
        $docFiles += @(Get-ChildItem -LiteralPath $p -File -Filter '*.md' -ErrorAction SilentlyContinue)
    }
}
$docFiles = @($docFiles | Sort-Object Name -Unique)
$hasAgents = Test-Path -LiteralPath (Join-Path $Project 'AGENTS.md')

# 4) 输出
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('# 产品/设计上下文（自动扫描线索）— ' + (Split-Path -Leaf $Project))
[void]$sb.AppendLine('')
[void]$sb.AppendLine('- 工程根：`' + $Project + '`')
[void]$sb.AppendLine('- 扫描时间：' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))
[void]$sb.AppendLine('- 文件预算：' + [string]$MaxFiles + '；实际扫描 ' + [string]$files.Count + ' 个源码文件' + $(if ($fileBudgetHit) { '（已截断，规模数据为下限）' } else { '' }))
[void]$sb.AppendLine('')
[void]$sb.AppendLine('> 自动扫描只给**线索**，不替代人工核对。设计前必须按 `references/55-design-intake.md` 补全 `design-context.md`。')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('## 1. 技术栈线索')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('| 类别 | 命中 |')
[void]$sb.AppendLine('|---|---|')
if ($hits.Count -eq 0) { [void]$sb.AppendLine('| （未识别） | 读 package.json 后人工补充 |') }
foreach ($h in $hits) { [void]$sb.AppendLine('| ' + $h[0] + ' | ' + $h[1] + ' |') }
[void]$sb.AppendLine('')
[void]$sb.AppendLine('## 2. 设计体系线索（需人工核实值）')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('| 线索 | 文件 |')
[void]$sb.AppendLine('|---|---|')
if ($themeFiles.Count -eq 0 -and $chartTheme.Count -eq 0) { [void]$sb.AppendLine('| 未发现 token/theme 文件 | 需读全局样式/组件库默认值 |') }
foreach ($f in @($themeFiles | Select-Object -First 10)) {
    [void]$sb.AppendLine('| token/theme | `' + $f.FullName.Replace($Project + '\', '') + '` |')
}
foreach ($f in @($chartTheme | Select-Object -First 5)) {
    [void]$sb.AppendLine('| 图表主题 | `' + $f.FullName.Replace($Project + '\', '') + '` |')
}
$styleTop = @($styleFileList)
if ($styleTop.Count -gt 0) {
    [void]$sb.AppendLine('| 样式文件数 | ' + [string]$styleTop.Count + '（前 5：' + (@($styleTop | Select-Object -First 5 | ForEach-Object { $_.Name }) -join ', ') + '） |')
}
[void]$sb.AppendLine('')
[void]$sb.AppendLine('## 3. 规模线索')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('| 项 | 数量 |')
[void]$sb.AppendLine('|---|---|')
[void]$sb.AppendLine('| 路由/路由文件 | ' + [string]$routerFiles + ' |')
[void]$sb.AppendLine('| API 文件 | ' + [string]$apiFiles + ' |')
[void]$sb.AppendLine('| 页面(view)文件 | ' + [string]$viewFiles + ' |')
[void]$sb.AppendLine('| mock 文件（数据缺口线索） | ' + [string]$mockFiles + ' |')
[void]$sb.AppendLine('| 样式文件 | ' + [string]$styleFiles + ' |')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('## 4. 文档与协作约定')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('| 项 | 结果 |')
[void]$sb.AppendLine('|---|---|')
[void]$sb.AppendLine('| AGENTS.md | ' + $(if ($hasAgents) { '存在（先读）' } else { '无（建议补协作契约）' }) + ' |')
[void]$sb.AppendLine('| Markdown 文档 | ' + [string]$docFiles.Count + '（' + (@($docFiles | Select-Object -First 6 | ForEach-Object { $_.Name }) -join ', ') + '） |')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('## 5. 待人工确认（复制到 design-context.md）')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('| # | 项 | 实测值 | 证据 |')
[void]$sb.AppendLine('|---|---|---|---|')
[void]$sb.AppendLine('| 1 | UI 框架/组件库/版本 | | package.json / 使用路径 |')
[void]$sb.AppendLine('| 2 | 主色/色板/间距/字号/圆角/阴影 | | theme/CSS 变量 |')
[void]$sb.AppendLine('| 3 | 布局骨架 | | 布局组件 + 截图 |')
[void]$sb.AppendLine('| 4 | 数据规范（精度/单位/时区/图表） | | 报表页 / chart-theme |')
[void]$sb.AppendLine('| 5 | 状态覆盖 | | 组件 props / 现有页面 |')
[void]$sb.AppendLine('| 6 | 样本页 3 个 | | 路径 + 截图 |')
[void]$sb.AppendLine('| 7 | 设计稿来源 | | Figma/蓝湖/无 |')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('## 6. 复现命令')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('```powershell')
[void]$sb.AppendLine('powershell -NoProfile -ExecutionPolicy Bypass -File "<skill>\scripts\product-context.ps1" -Project "' + $Project + '"')
[void]$sb.AppendLine('```')

try {
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($OutFile, $sb.ToString(), $enc)
    Write-Host ('[OK] 产品上下文线索已写入：' + $OutFile) -ForegroundColor Green
} catch {
    Write-Host ('[WARN] 写入失败：' + $_.Exception.Message) -ForegroundColor Yellow
}

Write-Host ''
Write-Host '技术栈线索：'
foreach ($h in $hits) { Write-Host ('  - ' + $h[0] + ': ' + $h[1]) }
Write-Host ('规模：路由 ' + $routerFiles + ' / API ' + $apiFiles + ' / view ' + $viewFiles + ' / mock ' + $mockFiles + ' / 样式 ' + $styleFiles)
Write-Host '提示：这些只是线索，下一步按 55-design-intake.md 填 design-context.md（含截图与 token 实测值）。' -ForegroundColor Gray
exit 0
