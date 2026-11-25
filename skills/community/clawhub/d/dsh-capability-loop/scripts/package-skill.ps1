# package-skill.ps1 — 生成「可上架 skill 商店」的发布包（校验 + 清单 + ZIP）
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File .\package-skill.ps1 [-SkillRoot <技能源目录>] [-OutDir <输出目录>] [-Handle <商店 handle>] [-Slug <商店 slug>] [-SkipZip] [-ExtraSensitivePaths <路径,...>]
# 退出码：0 = 校验通过且已打包；1 = 有 FAIL（未打包，或 ZIP 结构校验不合格）；2 = 参数错误
# 说明：只读技能源目录；输出到 <OutDir>（默认 <工作区>\dist\skill-store）。不改 DSH 安装目录、不自动发布。
[CmdletBinding()]
param(
    [string]$SkillRoot = '',
    [string]$OutDir = '',
    [string]$Handle = '',
    [string]$Slug = '',
    [switch]$SkipZip,
    [string[]]$ExtraSensitivePaths = @()
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version 2.0

$workspace = (Get-Location).Path
if (-not $SkillRoot) { $SkillRoot = Join-Path $workspace 'tools\capability-loop\skill\dsh-capability-loop' }
if (-not (Test-Path -LiteralPath $SkillRoot -PathType Container)) {
    Write-Host ('[FAIL] 技能源目录不存在：' + $SkillRoot) -ForegroundColor Red
    exit 2
}
$SkillRoot = (Resolve-Path -LiteralPath $SkillRoot).Path
if (-not $OutDir) { $OutDir = Join-Path $workspace 'dist\skill-store' }

function Read-Utf8 {
    param([string]$Path)
    try { return [System.IO.File]::ReadAllText($Path, (New-Object System.Text.UTF8Encoding($false))) } catch { return '' }
}
function Get-FrontmatterField {
    param([string]$Text, [string]$Field)
    $m = [regex]::Match($Text, '(?ms)^' + [regex]::Escape($Field) + ':\s*(.*?)(?=\r?\n[A-Za-z0-9_-]+:\s|\r?\n---)')
    if ($m.Success) { return ($m.Groups[1].Value -replace "`r?`n", ' ').Trim() }
    return ''
}

$issues = New-Object System.Collections.ArrayList
function Add-I {
    param([string]$Status, [string]$Item, [string]$Detail)
    $o = New-Object psobject
    $o | Add-Member -MemberType NoteProperty -Name Status -Value $Status
    $o | Add-Member -MemberType NoteProperty -Name Item -Value $Item
    $o | Add-Member -MemberType NoteProperty -Name Detail -Value $Detail
    [void]$issues.Add($o)
}

# 1) 必需文件
foreach ($f in @('SKILL.md', 'version.json', 'CHANGELOG.md', 'QUICKSTART.md')) {
    if (Test-Path -LiteralPath (Join-Path $SkillRoot $f)) { Add-I 'PASS' $f '存在' } else { Add-I 'FAIL' $f '缺少（商店包必需）' }
}
if (Test-Path -LiteralPath (Join-Path $SkillRoot 'README.md')) { Add-I 'PASS' 'README.md' '存在（商店详情/人读概览）' } else { Add-I 'WARN' 'README.md' '建议补（商店详情页与人读概览）' }

# 2) frontmatter 与版本
$sk = Read-Utf8 (Join-Path $SkillRoot 'SKILL.md')
$name = Get-FrontmatterField $sk 'name'
$desc = Get-FrontmatterField $sk 'description'
if ($name -match '^[a-z0-9][a-z0-9-]{0,63}$') { Add-I 'PASS' 'frontmatter name' $name } else { Add-I 'FAIL' 'frontmatter name' ('必须是 kebab-case：' + $name) }
if ($desc.Length -gt 0 -and $desc.Length -le 500) {
    if ($desc.Length -gt 200) { Add-I 'WARN' 'description 长度' ([string]$desc.Length + ' 字符（>200 偏贵，硬上限 500）') }
    else { Add-I 'PASS' 'description 长度' ([string]$desc.Length + ' 字符') }
} else { Add-I 'FAIL' 'description 长度' ('缺失或 >500：' + [string]$desc.Length) }

$verText = Read-Utf8 (Join-Path $SkillRoot 'version.json')
$verMatch = [regex]::Match($verText, '"version"\s*:\s*"([^"]+)"')
$version = ''
if ($verMatch.Success) { $version = $verMatch.Groups[1].Value }
if ($version -match '^\d+\.\d+\.\d+$') { Add-I 'PASS' 'version' $version } else { Add-I 'FAIL' 'version' ('必须是 semver x.y.z：' + $version) }
$nameMis = [regex]::Match($verText, '"name"\s*:\s*"([^"]+)"')
if ($nameMis.Success -and $nameMis.Groups[1].Value -ne $name) { Add-I 'FAIL' 'name 一致性' ('SKILL.md=' + $name + ' / version.json=' + $nameMis.Groups[1].Value) }
else { Add-I 'PASS' 'name 一致性' '一致' }

# frontmatter version 一致性：技能市场 declaredVersionOf 从 SKILL.md frontmatter 读 version 显示「已安装版本」。
$skVer = Get-FrontmatterField $sk 'version'
if ($skVer -ne '') {
    if ($skVer -eq $version) { Add-I 'PASS' 'frontmatter version' $skVer }
    else { Add-I 'FAIL' 'frontmatter version' ('SKILL.md=' + $skVer + ' / version.json=' + $version + '（必须一致）') }
}
else { Add-I 'WARN' 'frontmatter version' '未声明（市场「已安装版本」会显示为空；建议加 version 并与 version.json 一致）' }

# 3) CHANGELOG 有当前版本条目
$cl = Read-Utf8 (Join-Path $SkillRoot 'CHANGELOG.md')
if ($version -ne '' -and $cl -match ('## v' + [regex]::Escape($version))) { Add-I 'PASS' 'CHANGELOG 条目' ('包含 v' + $version) }
else { Add-I 'WARN' 'CHANGELOG 条目' ('未找到 v' + $version + ' 的条目（建议补）') }

# 3) scripts/*.ps1 必须 UTF-8 带 BOM（否则 PS 5.1 中文乱码、脚本解析失败）
$psFiles = @(Get-ChildItem -LiteralPath (Join-Path $SkillRoot 'scripts') -File -Filter '*.ps1' -ErrorAction SilentlyContinue)
if ($psFiles.Count -gt 0) {
    $noBom = @()
    foreach ($psFile in $psFiles) {
        $bytes = [System.IO.File]::ReadAllBytes($psFile.FullName)
        if (-not ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)) { $noBom += $psFile.Name }
    }
    if ($noBom.Count -eq 0) { Add-I 'PASS' 'PowerShell BOM' ([string]$psFiles.Count + ' 个脚本均带 BOM') }
    else { Add-I 'FAIL' 'PowerShell BOM' ('缺 BOM（PS 5.1 会乱码）：' + ($noBom -join ', ')) }
}

# 4) 敏感信息/本机路径扫描：像真实凭证的命中直接 FAIL（阻断打包）；本机路径只 WARN 由人工确认
# 只匹配「像真实凭证」的赋值；文档里的 $env:FAKE_API_KEY='dummy-local-key' 等示例不报。
$badPatterns = @(
    'DXXC_TOKEN_HUB_API_KEY\s*=\s*[^\s]',
    'ZJTD_TOKEN_HUB_API_KEY\s*=\s*[^\s]',
    'DEEPSEEK_API_KEY\s*=\s*[^\s]',
    'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY',
    'password\s*[:=]\s*[^\s''"]{6,}',
    'secret\s*[:=]\s*[^\s''"]{6,}'
)
# 本机路径：运行时从环境推导（不写死用户名/盘符）；额外路径用 -ExtraSensitivePaths 传入。
$userPaths = New-Object System.Collections.ArrayList
if ($env:USERPROFILE) { [void]$userPaths.Add($env:USERPROFILE.TrimEnd('\') + '\') }
if ($env:LOCALAPPDATA) { [void]$userPaths.Add($env:LOCALAPPDATA.TrimEnd('\') + '\') }
foreach ($ep in $ExtraSensitivePaths) { if ($ep) { [void]$userPaths.Add($ep) } }
$userPathPatterns = @(
    '[A-Za-z]:\\Users\\[^\\\s"'']+\\',
    '[A-Za-z]:\\Documents and Settings\\[^\\\s"'']+\\'
)
$fileList = @(Get-ChildItem -LiteralPath $SkillRoot -Recurse -File -ErrorAction SilentlyContinue)
# 打包排除：临时/构建/缓存/版本库/工程级状态不属于技能本体（v2.10.0 修复：此前 .tmp 会被打进包，1003 条目）。
# .dsh/ 是「接入本工程」的接管状态（含本机路径），属于工程而非技能，必须排除。
$excludeDirs = @('.tmp', '.git', '.dsh', 'dist', 'out', '__pycache__', 'node_modules', 'memory')
$excludeFiles = @('.DS_Store', 'Thumbs.db')
# 二进制/图片/压缩包/私钥不进包：既非技能运行所需，也会让安全扫描只能做部分分析。
$excludeExt = @('.png', '.jpg', '.jpeg', '.gif', '.zip', '.7z', '.pem', '.key')
$excludeRelPrefixes = @('plugins\capability-loop\test\')
$fileList = @($fileList | Where-Object {
    $rel = $_.FullName.Substring($SkillRoot.Length).TrimStart('\')
    $parts = $rel -split '\\'
    $skip = $false
    foreach ($p in $parts) { if ($excludeDirs -contains $p) { $skip = $true; break } }
    if ($skip) { return $false }
    if ($excludeFiles -contains $_.Name) { return $false }
    if ($excludeExt -contains $_.Extension.ToLowerInvariant()) { return $false }
    foreach ($pre in $excludeRelPrefixes) { if ($rel.StartsWith($pre, [System.StringComparison]::OrdinalIgnoreCase)) { return $false } }
    return $true
})
$credHits = @()
$pathHits = @()
foreach ($f in $fileList) {
    if ($f.Extension -in @('.md', '.json', '.ps1', '.txt', '.mjs', '.js', '.yml', '.yaml')) {
        $txt = Read-Utf8 $f.FullName
        foreach ($bp in $badPatterns) { if ($txt -match $bp) { $credHits += ($f.Name + ' 命中凭证模式 ' + $bp) } }
        # 本机路径按文件去重：%LOCALAPPDATA% 通常位于 %USERPROFILE% 下，逐个匹配会把同一处记成多条 WARN。
        $pathHit = ''
        foreach ($up in $userPaths) { if ($txt -match [regex]::Escape([string]$up)) { $pathHit = [string]$up; break } }
        if ($pathHit -eq '') {
            foreach ($up in $userPathPatterns) { if ($txt -match $up) { $pathHit = $matches[0]; break } }
        }
        if ($pathHit -ne '') { $pathHits += ($f.Name + ' 含本机路径 ' + $pathHit) }
    }
}
if ($credHits.Count -gt 0) {
    Add-I 'FAIL' '敏感信息扫描' ([string]$credHits.Count + ' 处疑似凭证（必须脱敏后才能打包）：' + (($credHits | Select-Object -First 3) -join '; '))
} else {
    Add-I 'PASS' '敏感信息扫描' '未发现疑似凭证'
}
if ($pathHits.Count -eq 0) { Add-I 'PASS' '本机路径扫描' '未发现' }
else { Add-I 'WARN' '本机路径扫描' ([string]$pathHits.Count + ' 处（上架前请人工确认是否需脱敏）：' + (($pathHits | Select-Object -First 5) -join '; ')) }

$failCount = @($issues | Where-Object { $_.Status -eq 'FAIL' }).Count
$warnCount = @($issues | Where-Object { $_.Status -eq 'WARN' }).Count

Write-Host ''
Write-Host '==== skill 商店发布校验 ====' -ForegroundColor Cyan
Write-Host ('源目录：' + $SkillRoot)
Write-Host ('版本  ：' + $(if ($version -ne '') { $version } else { '（未知）' }))
Write-Host ''
foreach ($i in $issues) {
    $color = 'Gray'
    if ($i.Status -eq 'PASS') { $color = 'Green' } elseif ($i.Status -eq 'WARN') { $color = 'Yellow' } elseif ($i.Status -eq 'FAIL') { $color = 'Red' }
    Write-Host ('  [' + $i.Status + '] ' + $i.Item + ' — ' + $i.Detail) -ForegroundColor $color
}
Write-Host ''
if ($failCount -gt 0) {
    Write-Host ('校验 FAIL（' + [string]$failCount + ' 项），不打包。修完后重跑。') -ForegroundColor Red
    exit 1
}

# 5) 打包
$pkgRoot = Join-Path $OutDir ('dsh-capability-loop-v' + $version)
if (Test-Path -LiteralPath $pkgRoot) { Remove-Item -LiteralPath $pkgRoot -Recurse -Force }
$pkgSkillDir = Join-Path $pkgRoot $name
New-Item -ItemType Directory -Force -Path $pkgSkillDir | Out-Null
foreach ($f in $fileList) {
    $rel = $f.FullName.Replace($SkillRoot + '\', '')
    $dst = Join-Path $pkgSkillDir $rel
    $d = Split-Path -Parent $dst
    if (-not (Test-Path -LiteralPath $d)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
    Copy-Item -LiteralPath $f.FullName -Destination $dst -Force
}

# 文件清单 + SHA256
$hashes = @()
foreach ($f in $fileList) {
    $rel = $f.FullName.Replace($SkillRoot + '\', '')
    $h = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
    $hashes += ('{0}  {1}' -f $h, $rel.Replace('\', '/'))
}

$storeBlock = 'null'
if ($Handle -ne '' -or $Slug -ne '') {
    $h2 = $Handle
    $s2 = $Slug
    if ($h2 -eq '') { $h2 = '<your-handle>' }
    if ($s2 -eq '') { $s2 = $name }
    $storeBlock = '{"handle":"' + $h2 + '","slug":"' + $s2 + '","id":"@' + $h2 + '/' + $s2 + '","install_dir":"' + $h2 + '--' + $s2 + '","update_owner":"market","auto_update":false}'
}

$manifest = @"
{
  "schema": "dsh-skill-store/1",
  "name": "$name",
  "version": "$version",
  "description": "$((Get-FrontmatterField $sk 'description') -replace '"', '\"')",
  "files": $($fileList.Count),
  "checksums": "SHA256SUMS.txt",
  "store": $storeBlock,
  "generated_at": "$((Get-Date).ToString('yyyy-MM-ddTHH:mm:ssK'))"
}
"@
[System.IO.File]::WriteAllText((Join-Path $pkgRoot 'manifest.json'), $manifest, (New-Object System.Text.UTF8Encoding($false)))
[System.IO.File]::WriteAllText((Join-Path $pkgRoot 'SHA256SUMS.txt'), (($hashes -join "`r`n") + "`r`n"), (New-Object System.Text.UTF8Encoding($false)))

$notes = @"
# 上架说明（skill 商店）

- 包内目录：``$name/``（SKILL.md 在根，name=$name，version=$version）
- **DSH 技能市场不是发布端**：它只浏览/安装 SkillHub 上的 skill。上架 = 用 ``clawhub`` CLI 发布到 ClawHub，SkillHub 同步后市场可搜到（见 ``references/95-store-publish.md``）。
- 上架命令（首次与更新同一条，**发布本包目录而不是源码仓库根**，避免带入 .git/.tmp/截图）：
  - ``npm.cmd i -g clawhub``
  - ``clawhub login``
  - ``clawhub skill publish "<本包目录>\$name" --slug "$name" --name "$name" --version "$version" --changelog "v${version}: <摘要>"``
- 本 ZIP 用于：**本地导入**（只含技能目录，单一顶层 ``<name>/``，可被市场直接导入）/留档/离线分发；``manifest.json``/``SHA256SUMS.txt``/``PUBLISH-NOTES.md`` 在包目录留档，**不进 ZIP**；**上架 ClawHub 不需要 ZIP**，直接发布目录。
- 上架后商店安装目录通常是 ``<handle>--<slug>``（如 ``your-handle--$name``）；这是 DSH 技能市场的命名约定，``name`` frontmatter 不变。
- **若 manifest 的 store.id 仍是 ``<handle>``/``your-handle`` 占位，正式上架前请用真实 handle 重跑本脚本**（``-Handle``），否则商店记录与包内元数据不一致。
- 更新由**商店负责**：安装/更新/回滚都在商店 UI 完成；技能自身不自动更新，也不覆盖用户修改。
- 版本一致性：``version.json`` 为权威；``SKILL.md`` frontmatter 的 ``version`` 必须与之相同（技能市场据此显示「已安装版本」，缺失则显示为空）；``CHANGELOG.md`` 需有对应版本条目。
- 发布前检查：SKILL.md frontmatter name/description/权限声明合法；version.json 与 CHANGELOG 版本一致；``README.md``/``QUICKSTART.md`` 与版本一致。
- **打包排除（脚本硬编码）**：``.tmp``/``.git``/``.dsh``/``dist``/``out``/``node_modules``/``__pycache__``/``memory``（用户偏好记忆不进包）、图片/压缩包/私钥（``.png/.jpg/.jpeg/.gif/.zip/.7z/.pem/.key``）、插件夹具 ``plugins/capability-loop/test/``。
- **敏感扫描是启发式**：疑似凭证命中会 FAIL 并阻断打包；本机绝对路径只 WARN，仍需人工复核。包内不含会话库、DSH storage、备份或用户凭据。
- 权限与数据边界见包内 ``SECURITY.md``（写哪些目录、起哪些子进程、是否联网、如何删除记忆）。
- 校验和：见 ``SHA256SUMS.txt``；单文件哈希在 ``manifest.json`` 之外提供，商店可复用。
- 回滚：商店版本历史可安装旧版本；技能自身 ``CHANGELOG.md`` 记录每个版本的变更与回滚方式。
"@
[System.IO.File]::WriteAllText((Join-Path $pkgRoot 'PUBLISH-NOTES.md'), $notes, (New-Object System.Text.UTF8Encoding($false)))

$zipPath = ''
if (-not $SkipZip) {
    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zipPath = Join-Path $OutDir ('dsh-capability-loop-v' + $version + '.zip')
    if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
    # 手工写条目：ZIP 规范要求路径分隔符为 '/'（PS5.1 的 CreateFromDirectory 在 .NET Framework 下会写成 '\'）
    # 只收技能目录、保持单一顶层 <name>/：市场「本地导入」靠单一顶层剥壳才能找到 SKILL.md；
    # manifest/SHA256SUMS/PUBLISH-NOTES 留在包目录供留档，不进 ZIP。
    $archive = $null
    try {
        $archive = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
        foreach ($zf in @(Get-ChildItem -LiteralPath $pkgSkillDir -Recurse -File)) {
            $rel = $name + '/' + $zf.FullName.Substring($pkgSkillDir.Length + 1).Replace('\', '/')
            [void][System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $zf.FullName, $rel, [System.IO.Compression.CompressionLevel]::Optimal)
        }
    } catch {
        Write-Host ('[FAIL] ZIP 生成失败：' + $_.Exception.Message) -ForegroundColor Red
        exit 1
    } finally {
        if ($archive -ne $null) { $archive.Dispose() }
    }
    if (-not (Test-Path -LiteralPath $zipPath)) {
        Write-Host '[FAIL] ZIP 未生成（路径不存在）' -ForegroundColor Red
        exit 1
    }
    $za = $null
    $entryCount = 0
    $badSep = 0
    $topCount = 0
    try {
        $za = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
        $entryCount = $za.Entries.Count
        $badSep = @($za.Entries | Where-Object { $_.FullName -like '*\*' }).Count
        $topCount = @($za.Entries | ForEach-Object { ($_.FullName -split '/')[0] } | Sort-Object -Unique).Count
    } catch {
        Write-Host ('[WARN] ZIP 条目校验失败：' + $_.Exception.Message) -ForegroundColor Yellow
    } finally {
        if ($za -ne $null) { $za.Dispose() }
    }
    $zipProblems = @()
    if ($entryCount -eq 0) { $zipProblems += 'ZIP 为 0 条目（技能目录为空或复制失败）' }
    if ($badSep -gt 0) { $zipProblems += ('ZIP 有 ' + [string]$badSep + ' 个条目使用反斜杠路径（应为 /）') }
    if ($topCount -ne 1) { $zipProblems += ('ZIP 有 ' + [string]$topCount + ' 个顶层目录（本地导入要求单一顶层 <name>/）') }
    if ($zipProblems.Count -gt 0) {
        foreach ($p in $zipProblems) { Write-Host ('[FAIL] ' + $p) -ForegroundColor Red }
        Write-Host '[FAIL] ZIP 结构不合格，不能作为商店包/本地导入包（市场会报「技能包缺少 SKILL.md」）。' -ForegroundColor Red
        exit 1
    }
    Write-Host ('ZIP 校验：' + [string]$entryCount + ' 个条目，路径分隔符均为 /，单一顶层 ' + $name + '/') -ForegroundColor Gray
}

Write-Host ('包目录：' + $pkgRoot) -ForegroundColor Green
if ($zipPath -ne '') { Write-Host ('ZIP   ：' + $zipPath) -ForegroundColor Green }
Write-Host ('文件数：' + [string]$fileList.Count + '；SHA256SUMS 已生成；WARN=' + [string]$warnCount) -ForegroundColor Gray
Write-Host ''
Write-Host '下一步：clawhub login → clawhub skill publish "<技能目录>" --slug <slug> --changelog "<摘要>"（ZIP 仅用于本地导入/留档；见 references/95-store-publish.md）。' -ForegroundColor Gray
exit 0
