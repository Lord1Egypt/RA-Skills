---
name: app-packager
description: >
  自动切换 Git 分支并执行 APP 打包脚本。支持指定分支、平台、构建类型、版本号、上传选项、API_KEY和更新说明。
  打包完成后会自动通知用户结果。
  Use when: 用户需要打包 APP、切换分支打包、构建应用、生成安装包。
  NOT for: 代码合并、代码提交、单元测试、代码检查。
---

# APP 打包助手（带完成通知）

## 执行方式

### 方式一：命令行调用（推荐）
```bash
~/.openclaw/workspace/skills/app-packager/scripts/app-packager --branch develop --platform android --upload --api-key 你的API_KEY --desc "更新说明"
```

**重要**：所有打包都必须使用此脚本，不要手动执行 `pgyer_all.sh`！

**参数选项：**
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--branch` | `-b` | Git 分支 | develop |
| `--platform` | `-p` | 平台 (android/ios/all) | all (双端打包) |
| `--type` | - | 构建类型 (debug/adhoc/release) | debug |
| `--upload` | `-u` | 上传到蒲公英 | 否 |
| `--api-key` | `--key` | 蒲公英 API_KEY | - |
| `--desc` | `-d` | 更新说明 | - |

### 方式二：自然语言触发
直接对我说："在 develop 分支打包 Android" 或 "打包 iOS release 版"

## When to Run
- 用户说“打包 APP”“生成安装包”“构建应用”
- 用户说“在 xx 分支上打包”“切到 xx 分支打包”
- 用户指定平台如“打包 iOS”“打安卓包”
- 用户指定类型如“打 debug 包”“打 release 包”
- 用户指定版本如“版本 1.2.3 打包”
- 用户指定 API_KEY 如“api_key: xxxxx”
- 用户说“打渠道包”

## Pre-flight Check（执行前检查）
1. 确认项目路径：`/Users/nuoyun/Desktop/package/NYLiveUser` 是否存在
2. 确认打包脚本：`./pgyer_all.sh` 是否有执行权限
3. 确认 Git 命令可用

## Workflow

### 第一步：解析用户意图
从用户输入中提取所有参数，使用以下规则：

#### 参数提取规则
- **分支 (branch)**: 匹配 `在\s*([\w\-_\./]+)\s*分支` 或 `切到\s*([\w\-_\./]+)\s*分支` 或 `分支[:：]\s*([\w\-_\./]+)`
- **版本号 (version)**: 匹配 `版本[:：]?\s*([\d\.]+)` 或 `version[:：]?\s*([\d\.]+)`
- **构建类型 (build_type)**: 匹配 `debug|测试包|测试版本` → `debug`; `adhoc|验收包|验收版本` → `adhoc`; `release|发布包|发布版本|商店包` → `release`
- **平台 (platform)**: 匹配 `iOS|苹果|iphone` → `ios`; `安卓|android` → `android`; `渠道包|多渠道` → `channel`; 未指定时 → ``（双端打包）
- **是否上传 (upload)**: 匹配 `上传|需要上传|要上传` → `yes`; `不上传|不需要上传|不用上传` → `no`
- **API_KEY (api_key)**: 匹配 `api_key[:：]\s*([a-zA-Z0-9_\-]+)` 或 `API密钥[:：]\s*([a-zA-Z0-9_\-]+)` 或 `蒲公英密钥[:：]\s*([a-zA-Z0-9_\-]+)`
- **更新说明 (desc)**: 匹配 `说明[:：]\s*(.+?)(?=\.|$|，|。)` 或 `描述[:：]\s*(.+?)(?=\.|$|，|。)` 或 `更新内容[:：]\s*(.+?)(?=\.|$|，|。)`

#### 特殊判断
- **渠道包**：如果 `platform` 为 `channel`，设置 `is_channel_package=true`

### 第二步：参数处理规则

**基本原则**：每个参数独立判断，用户指定就用指定的值，否则用脚本默认值。

| 脚本提示 | 参数变量 | 用户指定时的映射 | 默认行为 |
|---------|---------|-----------------|---------|
| 版本号 | `version` | 直接填入用户输入的版本号 | 直接回车（脚本读取 pubspec.yaml） |
| 构建类型 | `build_type` | `debug`→`1`, `adhoc`→`2`, `release`→`3` | 直接回车（脚本默认） |
| 平台选择 | `platform` | `ios`→`1`, `android`→`2`, 渠道包→`3` | 直接回车（脚本默认：双端打包） |
| 是否上传 | `upload` | `yes`→`1`, `no`→`2` | 直接回车（默认：不上传） |
| API_KEY | `api_key` | 直接填入用户输入的 API_KEY | 直接回车（用脚本默认值） |
| 更新说明 | `desc` | 直接填入用户输入的说明 | 直接回车（空字符串） |

### 第三步：执行打包流程

```bash
# 进入项目目录
cd /Users/nuoyun/Desktop/package/NYLiveUser/ || { 
    reply "❌ 错误：项目路径 /Users/nuoyun/Desktop/package/NYLiveUser/ 不存在"
    exit 1
}

# 检查脚本权限
if [ ! -x "./pgyer_all.sh" ]; then
    reply "❌ 错误：打包脚本 pgyer_all.sh 无执行权限，请执行：chmod +x pgyer_all.sh"
    exit 1
fi

# 切换分支（如果指定了分支）
branch_status=""
if [ -n "$branch" ]; then
    reply "🔄 正在切换到分支: $branch ..."
    
    # 先拉取最新代码
    git fetch --all
    
    # 检查分支是否存在
    if git show-ref --verify --quiet refs/heads/"$branch"; then
        # 本地分支存在
        git checkout "$branch"
        git pull origin "$branch"
        branch_status="✅ 已切换到本地分支: $branch"
    elif git ls-remote --exit-code --heads origin "$branch"; then
        # 远程分支存在，创建本地分支并跟踪
        git checkout -b "$branch" origin/"$branch"
        branch_status="✅ 已切换到远程分支: $branch"
    else
        # 分支不存在
        reply "❌ 错误：分支 '$branch' 不存在"
        exit 1
    fi
else
    current_branch=$(git branch --show-current)
    branch_status="📌 保持当前分支: $current_branch"
fi

# 显示当前分支状态
git status -sb

# 记录开始时间
start_time=$(date +%s)

# 告知用户开始打包
reply "🚀 开始打包，预计需要3-5分钟，完成后我会通知您～"

# 构建输入序列
inputs=()

# 1. 版本号
if [ -n "$version" ]; then
    inputs+=("$version")
else
    inputs+=("")
fi

# 2. 构建类型
if [ "$build_type" = "debug" ]; then
    inputs+=("1")
elif [ "$build_type" = "adhoc" ]; then
    inputs+=("2")
elif [ "$build_type" = "release" ]; then
    inputs+=("3")
else
    inputs+=("")
fi

# 3. 平台选择
if [ "$is_channel_package" = "true" ]; then
    inputs+=("3")
else
    if [ "$platform" = "ios" ]; then
        inputs+=("1")
    elif [ "$platform" = "android" ]; then
        inputs+=("2")
    else
        inputs+=("")
    fi
fi

# 4. 如果不是渠道包，才需要后续三个参数
if [ "$is_channel_package" != "true" ]; then
    # 4.1 是否上传
    if [ "$upload" = "yes" ]; then
        inputs+=("1")
    elif [ "$upload" = "no" ]; then
        inputs+=("2")
    else
        inputs+=("2")  # 默认不上传（对应脚本中的选项2）
    fi
    
    # 4.2 API_KEY - 接收用户输入，没有指定时用默认
    if [ -n "$api_key" ]; then
        inputs+=("$api_key")
    else
        inputs+=("")  # 回车，使用脚本默认值
    fi
    
    # 4.3 更新说明
    if [ -n "$desc" ]; then
        inputs+=("$desc")
    else
        inputs+=("")
    fi
fi

# 执行打包并捕获输出
temp_output=$(mktemp)
temp_error=$(mktemp)

# 构建输入字符串
input_string=""
for item in "${inputs[@]}"; do
    input_string+="$item\n"
done

# 执行打包命令
echo -e "$input_string" | ./pgyer_all.sh > "$temp_output" 2> "$temp_error"
exit_code=$?

# 计算耗时
end_time=$(date +%s)
duration=$((end_time - start_time))
minutes=$((duration / 60))
seconds=$((duration % 60))
time_str="${minutes}分${seconds}秒"

# 读取输出内容
output_content=$(cat "$temp_output")
error_content=$(cat "$temp_error")

# 清理临时文件
rm -f "$temp_output" "$temp_error"

# 分析打包结果并生成反馈
if [ $exit_code -eq 0 ]; then
    # 打包成功，提取生成的文件信息
    apk_files=$(find /Users/nuoyun/Desktop/package/NYLiveUser/build -name "*.apk" -type f -mmin -5 2>/dev/null | head -3)
    ipa_files=$(find /Users/nuoyun/Desktop/package/NYLiveUser/build -name "*.ipa" -type f -mmin -5 2>/dev/null | head -3)
    
    # 提取蒲公英链接
    pgyer_links=$(echo "$output_content" | grep -E "https?://[a-zA-Z0-9./-]+(pgyer|蒲公英)" | head -3)
    
    # 构建成功消息
    feedback="✅ 打包完成！\n\n"
    feedback+="📂 分支信息：$branch_status\n"
    feedback+="⏱️ 打包耗时：$time_str\n\n"
    feedback+="📦 打包参数：\n"
    
    # 版本号
    if [ -n "$version" ]; then
        feedback+="• 版本号：$version\n"
    else
        feedback+="• 版本号：默认(取自pubspec.yaml)\n"
    fi
    
    # 构建类型
    if [ -n "$build_type" ]; then
        feedback+="• 构建类型：$build_type\n"
    else
        feedback+="• 构建类型：默认(iOS debug/Android release)\n"
    fi
    
    # 平台
    if [ "$is_channel_package" = "true" ]; then
        feedback+="• 平台：渠道包(Android多渠道)\n"
    elif [ -n "$platform" ]; then
        feedback+="• 平台：$platform\n"
    else
        feedback+="• 平台：双端(iOS+Android)\n"
    fi
    
    # 上传
    if [ "$is_channel_package" = "true" ]; then
        feedback+="• 上传蒲公英：不适用(渠道包自动跳过)\n"
    elif [ -n "$upload" ]; then
        if [ "$upload" = "yes" ]; then
            feedback+="• 上传蒲公英：是\n"
        else
            feedback+="• 上传蒲公英：否\n"
        fi
    else
        feedback+="• 上传蒲公英：否(默认)\n"
    fi
    
    # API_KEY（只在用户指定或上传为是时显示）
    if [ "$is_channel_package" != "true" ] && [ "$upload" = "yes" ]; then
        if [ -n "$api_key" ]; then
            feedback+="• API_KEY：$api_key\n"
        else
            feedback+="• API_KEY：使用默认值\n"
        fi
    fi
    
    # 更新说明
    if [ "$is_channel_package" = "true" ]; then
        feedback+="• 更新说明：不适用\n"
    elif [ -n "$desc" ]; then
        feedback+="• 更新说明：$desc\n"
    else
        feedback+="• 更新说明：无\n"
    fi
    
    feedback+="\n📁 生成文件：\n"
    
    # 添加APK文件
    if [ -n "$apk_files" ]; then
        while IFS= read -r apk; do
            feedback+="📱 Android: \`$apk\`\n"
        done <<< "$apk_files"
    fi
    
    # 添加IPA文件
    if [ -n "$ipa_files" ]; then
        while IFS= read -r ipa; do
            feedback+="🍎 iOS: \`$ipa\`\n"
        done <<< "$ipa_files"
    fi
    
    # 添加蒲公英链接
    if [ -n "$pgyer_links" ] && [ "$upload" = "yes" ]; then
        feedback+="\n📎 下载链接：\n"
        while IFS= read -r link; do
            feedback+="$link\n"
        done <<< "$pgyer_links"
    fi
    
    feedback+="\n💡 提示：文件保存在 build 目录下，可通过 Finder 访问。"
else
    # 构建失败消息
    error_summary=$(echo "$error_content" | tail -20)
    
    feedback="❌ 打包失败\n\n"
    feedback+="📂 分支信息：$branch_status\n"
    feedback+="⏱️ 耗时：$time_str\n\n"
    feedback+="❌ 错误信息：\n\`\`\`\n"
    feedback+="$error_summary\n"
    feedback+="\`\`\`\n\n"
    feedback+="🔍 可能的原因：\n"
    feedback+="1. 代码编译错误 - 检查 Flutter 环境\n"
    feedback+="2. 依赖问题 - 尝试执行 \`flutter pub get\`\n"
    feedback+="3. iOS 证书问题 - 检查证书配置\n"
    feedback+="4. Android 签名问题 - 检查 keystore 配置\n\n"
    feedback+="📋 完整日志：请查看项目目录下的 build.log 文件"
fi

# 发送反馈消息
reply "$feedback"
