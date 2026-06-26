---
name: code-review
description: Complete code review workflow for GitCode PRs. Combines automated security scanning with manual code review, outputs formatted findings, and posts comments to PR. Use when reviewing GitCode pull requests - follows 5-step process: automated scan, manual review, issue selection, formatted output, and optional PR comment posting.
---

# Code Review Skill

Complete 5-step code review workflow for GitCode PRs.

## 📁 Temp Directory Management

**所有审查过程中生成的临时文件必须存放在 `temp/` 目录下**：

| 文件 | 说明 |
|:---|:---|
| `temp/review_result.json` | Step 1 自动化扫描结果 |
| `temp/top3_issues.json` | Step 3 选择的 Top 问题 |
| `temp/formatted_review.json` | Step 4 格式化后的评论 |
| `temp/*.py` | 脚本运行时缓存的文件 |
| `temp/*` | 获取的 diff 文件，下载的代码文件 |

**⚠️ 重要**：审查完成后必须清理 `temp/` 目录，删除所有临时文件。

## 5-Step Review Process

### Step 1: Automated Scanning

Run script to detect critical issues:

```bash
python scripts/review_pr.py <pr_url> [token]
```

Detects: SQL injection, command injection, XSS, eval(), hardcoded credentials, resource leaks, infinite loops.

**Features**:
- ✅ **Automatic line number verification** - Downloads the actual file and verifies line numbers match the code snippets
- ✅ **Smart caching** - Avoids redundant downloads for the same PR
- ✅ **Line number correction** - Automatically fixes incorrect line numbers and logs changes

**Output**: `temp/review_result.json` (with verified line numbers)

### Step 2: Manual Review (REQUIRED)

**Always read all changed code manually.** Script misses:

- Logic errors and edge cases
- Design flaws
- Performance issues
- Missing error handling
- Business logic errors
- Code duplication
- Test coverage gaps

**How to get diff**:

```bash
curl -H "Authorization: Bearer <token>" \
  "https://gitcode.com/api/v5/repos/<owner>/<repo>/pulls/<number>/diff"
```

**Important**: For each issue found, record:

- **File path**: e.g., `src/components/Table.tsx`
- **Line range**: e.g., `L42-L45` (the line numbers of the problematic code)
- **Problem code**: The actual code snippet
- **Description**: Detailed explanation of the issue
- **Suggestion**: Specific fix recommendation

**How to find the correct line number in the new file**:

Use the provided helper script to find exact line numbers:

```bash
# Single line
python scripts/find_line_numbers.py <file_path> "code snippet"

# Multi-line (use \n to separate lines)
python scripts/find_line_numbers.py <file_path> "line1\nline2\nline3"
```

**Example**:
```bash
python scripts/find_line_numbers.py file_parser.py "return entries"
# Output: 第 119 行

python scripts/find_line_numbers.py file_parser.py "line.startswith('[ERROR] HCCL') or\n                        line.startswith('[INFO] HCCL')"
# Output: 第 103-104 行
```

**Important**: The `position` in your JSON must be the **last line** of the problematic code range (e.g., if problem spans L103-L105, use `105`).

**Manual method** (if script unavailable):

When reviewing a diff file, the line numbers shown in the diff (after `@@` markers) may not match the actual line numbers in the new file. To find the correct `position` for PR comments:

**Understanding diff hunk headers**:
```
@@ -old_start,old_count +new_start,new_count @@
```
- `-old_start,old_count`: Old file starting line and number of lines
- `+new_start,new_count`: New file starting line and number of lines

**How to calculate exact line numbers in the new file**:

1. Find the hunk header with `+new_start` (the number after `+`)
2. Count lines from that starting number, **including**:
   - Context lines (no prefix)
   - Added lines (starting with `+`)
   - Modified lines (shown as removed `-` then added `+`)
3. **Exclude** the hunk header line itself and file metadata lines

**Example**:
```
@@ -40,7 +39,7 @@ bool QueryTableDataDetailHandler::HandleRequest(...)
     } else if (request.params.type == "1") {
         ComputeLinkPageDetail(request, response, database);
     }
-    session.OnResponse(std::move(responsePtr));
+    SendResponse(std::move(responsePtr), true);
     return true;
 }
```
- New file starts at line 39
- Line 39: `} else if ...`
- Line 40: `ComputeLinkPageDetail...`
- Line 41: `}`
- Line 42: `SendResponse(std::move(responsePtr), true);` ← **This is line 42**
- Line 43: `return true;`

2. **For new files** (file mode is `new file mode`):
   ```powershell
   # Count only lines starting with '+' (excluding '+++ ' header)
   $lines = Get-Content pr_diff.txt
   $inFile = $false
   $lineNum = 0
   for ($i = 0; $i -lt $lines.Count; $i++) {
       if ($lines[$i] -match "^diff --git.*your-file.py") { $inFile = $true }
       if ($inFile -and $lines[$i] -match "^\+.*your-target-code") {
           Write-Output "New file line: $lineNum"
           break
       }
       if ($inFile -and $lines[$i] -match "^\+" -and $lines[$i] -notmatch "^\+\+\+") {
           $lineNum++
       }
   }
   ```

3. **Quick check**: The `position` should point to the **last line** of the problematic code range in the **new file** (after PR changes).

**Tip**: If GitCode API returns `400 Bad Request` with "diff failed to be generated due to invalid params under position param", the line number is likely incorrect.

**Important**: Always verify by manually counting from the `+new_start` line number in the hunk header. Do not guess or estimate line numbers.

### Step 3: Select Top 3 Issues

**⚠️ 流程决策**：

| 问题数量 | 后续步骤 |
|:---|:---|
| **0 个** | 直接退出，输出"0 问题，审查通过"，跳过 Step 3/4/5 |
| **1-3 个** | 继续 Step 3/4，按实际数量处理（不必凑满 3 个） |
| **>3 个** | 选择最严重的 3 个问题，继续后续步骤 |

Combine automated + manual findings:

- Filter false positives from script
- Add issues found in manual review
- Sort by severity (1-10)
- Select top issues (up to 3, no need to fill exactly 3)

**Note**: 当问题数量为 0 时，**直接退出整个审查流程**，无需生成任何 JSON 文件。

Generate json format file `temp/top3_issues.json` for these issues to use in next step.

`temp/top3_issues.json` must be created in the directory of `format_review.py` for the next step to read.

**Important**:

- The `description` field must contain the **complete description** from Step 1 and Step 2 findings, not a simplified version. Include all context and details.
- The `position` field must be the **last line number** of the problematic code range (e.g., if problem code is at L42-L45, use `45`)

**Structure**:

```json
{
  "meta": {
    "total_issues": 5,
    "selected_issues": 3,
    "automated_count": 2,
    "manual_count": 3
  },
  "top3_issues": [
    {
      "number": 1,
      "path": "src/file.py",
      "lines": "L42-L45",
      "position": 45,
      "severity": 8,
      "type": "安全问题",
      "description": "Complete description from Step 1/2 findings, not simplified",
      "suggestion": "Detailed suggestion with specific actions",
      "code": "problematic code snippet from L42-L45",
      "code_context": ""
    }
    // 问题数量可以是 1-3 个，不必强制凑满 3 个
  ]
}
```

**Note**: `position` uses the **last line** of the code range for GitCode API positioning.

**Important**: The `position` must be the line number in the **new file** (after PR changes), not the line number in the diff file. See Step 2 for how to calculate the correct line number.

**If total issues = 0**: 跳过整个 Step 3/4/5，直接输出审查通过结论。

**If total issues 1-3**: 按实际数量继续后续步骤，无需凑满 3 个。

**After generating `temp/top3_issues.json`, display the issues in Markdown format**:

## Top 3 Issues Selected

---

### 🔴 问题 #1 | 可维护性问题 | 6/10

**文件**: `server/src/.../CheckProjectValidHandler.cpp`\*\*

**问题代码行**: `L119-L124`

**问题代码**:

```cpp
bool CheckProjectValidHandler::CheckPathSafety(
    const std::string& path,
    ProjectErrorType& error)
{
    ...
}
```

| review | 内容                         |
| :----- | :--------------------------- |
| 描述   | 代码重复，违反DRY原则        |
| 建议   | 提取公共函数到 FileUtil 类中 |

---

### 🟠 问题 #2 | 测试覆盖问题 | 6/10

**文件**: `server/src/.../CheckProjectValidHandler.cpp`\*\*

**问题代码行**: `L119`

**问题代码**:

```cpp
bool CheckProjectValidHandler::CheckPathSafety
```

| review | 内容                     |
| :----- | :----------------------- |
| 描述   | 缺少单元测试             |
| 建议   | 补充单元测试覆盖各种场景 |

---

### 🟡 问题 #3 | 代码一致性问题 | 5/10

**文件**: `server/src/.../TimelineProtocolRequest.h`\*\*

**问题代码行**: `L68-L72`

**问题代码**:

```cpp
bool isSafePath = std::any_of(path.begin(), path.end(), ...)
```

| review | 内容                                |
| :----- | :---------------------------------- |
| 描述   | 逻辑不一致，缺少 IsRegularFile 检查 |
| 建议   | 统一使用 FileUtil::CheckPathSafety  |

---

**Total**: 3 issues selected (or actual count if less than 3)

**Note**: `position` in JSON uses the last line number (e.g., L119-L124 → position: 124)

**After generating `temp/top3_issues.json`, immediately proceed to Step 4 to format the output.**

**If total issues = 0**: 直接跳过 Step 3/4/5，输出审查通过结论。

### Step 4: Format Output

Format issues to structured JSON:

```bash
python scripts/format_review.py temp/top3_issues.json temp/formatted_review.json
```

**Input**:

- `temp/top3_issues.json` from Step 3

**Output**: `temp/formatted_review.json`

`temp/formatted_review.json` must be created in the directory of `post_review.py` for the next step to read.

**Structure**:

```json
{
  "comments": [
    {
      "number": 1,
      "path": "src/file.py",
      "position": 42,
      "severity": 8,
      "type": "安全问题",
      "body": "【review】..."
    }
  ]
}
```

**Comment Format** (in `body` field):

```markdown
【review】{问题类型}。{问题描述}。{修改建议}。
```

**After generating `formatted_review.json`, display the formatted content**:

```
Step 4: Formatted Review Comments (Ready to Post)

以下 3 条评论将提交到 PR:

1. `CheckProjectValidHandler.cpp:119`
   类型: 可维护性问题 | 严重程度: 6/10
   内容: 【review】代码重复，违反DRY原则...

2. `CheckProjectValidHandler.cpp:119`
   类型: 测试覆盖问题 | 严重程度: 6/10
   内容: 【review】缺少单元测试...

3. `TimelineProtocolRequest.h:68`
   类型: 代码一致性问题 | 严重程度: 5/10
   内容: 【review】逻辑不一致...

Output: formatted_review.json
```

### Step 5: Post to PR (Optional) - ⚠️ 必须等待用户确认

**🚨 重要警告**：此步骤涉及向 PR 发布评论，属于外部写入操作。**必须先显示预览并等待用户明确确认（yes/no），严禁擅自执行！**

Preview and confirm before posting:

```bash
python scripts/post_review.py <owner> <repo> <pr_number> <token> [temp/formatted_review.json]
```

**Parameters**:

- `owner`: Repository owner (e.g., `Ascend`)
- `repo`: Repository name (e.g., `msinsight`)
- `pr_number`: PR number (e.g., `277`)
- `token`: GitCode access token
- `temp/formatted_review.json`: Output from Step 4 (default: `temp/formatted_review.json`)

**Example**:

```bash
python scripts/post_review.py Ascend msinsight 277 your_token_here temp/formatted_review.json
```

**Flow** (必须严格遵守):

1. Read `temp/formatted_review.json` from Step 4
2. Display preview of all comments
3. **⚠️ 必须等待用户明确确认**：询问用户 "是否确认提交以上评论？(yes/no)"
4. **只有用户回复 'yes' 或 '是' 后才执行提交**，否则取消
5. **审查完成后清理 temp 目录**（见下方）

---

## 🧹 Temp Directory Cleanup

**⚠️ 审查完成后必须清理 temp 目录**：

```bash
# 删除 temp 目录及其所有内容
Remove-Item -Recurse -Force temp/
# 或
rm -rf temp/
```

**清理时机**：
- 当问题数量为 **0** 时，审查通过后立即清理
- 当问题数量 **>0** 时，完成 Step 5（发布评论）后清理
- 如果用户**拒绝发布评论**，也需清理

**保留情况**：无

---

## Severity Scale

| Score | Level    | Action                 |
| ----- | -------- | ---------------------- |
| 9-10  | Critical | Block merge            |
| 7-8   | High     | Strongly recommend fix |
| 5-6   | Medium   | Recommend fix          |
| 3-4   | Low      | Optional fix           |
| 1-2   | Nit      | Style suggestion       |

---

## Manual Review Checklist

### Logic & Correctness

- [ ] Edge cases (null, empty, max values)
- [ ] Error handling paths
- [ ] Concurrency/thread safety
- [ ] Resource cleanup

### Design & Architecture

- [ ] Single responsibility
- [ ] No code duplication
- [ ] Clean interfaces
- [ ] Clear dependencies

### Performance

- [ ] Algorithm complexity
- [ ] N+1 queries
- [ ] Large data handling
- [ ] Memory usage

### Security

- [ ] Input validation
- [ ] Output encoding
- [ ] Authorization checks
- [ ] Sensitive data handling

### Testing

- [ ] Tests cover changes
- [ ] Edge cases tested
- [ ] Error paths tested

---

## API Reference

- **Get PR files**: `GET /api/v5/repos/{owner}/{repo}/pulls/{number}/files`
- **Get diff**: `GET /api/v5/repos/{owner}/{repo}/pulls/{number}/diff`
- **Post comment**: `POST /api/v5/repos/{owner}/{repo}/pulls/{number}/comments`

---

## Scripts

| Script                | Purpose                   | Step | Input                       | Output                  | Features |
| --------------------- | ------------------------- | ---- | --------------------------- | ----------------------- | -------- |
| `review_pr.py`        | Automated scanning        | 1    | PR URL + Token              | `temp/review_result.json`    | Auto line verification, caching |
| `find_line_numbers.py`| Find code line numbers    | 2    | File path + code snippet    | Line number(s)          | Exact match, multi-line support |
| `format_review.py`    | Format to JSON            | 4    | `temp/top3_issues.json`     | `temp/formatted_review.json` | GitCode API format |
| `post_review.py`      | Post to PR                | 5    | `temp/formatted_review.json`| PR comments             | Batch posting with confirmation |

### Script Details

#### `review_pr.py`

**New Features** (v2.0):
1. **Automatic Line Number Verification**
   - Downloads modified files from PR branch
   - Uses code snippets to find exact line numbers
   - Corrects mismatches automatically

2. **File Caching**
   - Caches downloaded files to avoid redundant API calls
   - Cache key: `{owner}/{repo}/{sha}/{file_path}`

3. **Verification Logging**
   - Logs line number corrections: `Line number corrected: file.ts:275 -> 167`
   - Warns if verification fails
