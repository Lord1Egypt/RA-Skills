# CodeQL Python 安全查询的「敏感数据」名字启发式
# CodeQL Python security queries: the "sensitive data" name heuristic

> This is the sheet you will come back to most often: **which variable names make CodeQL decide that
> "this is sensitive data"**.
> 本文件是排查时最常回查的一张表：**哪些变量名会让 CodeQL 认定「这是敏感数据」**。
>
> All identifiers in this document are **synthetic examples**. None of them come from a real project.
> 本文出现的标识符**全部是构造出来的示例**，不来自任何真实项目。
>
> **Language / 语言**：本文档为双语，仅为可读性；工具运行时的输出语言由用户通过 `--lang` 控制（默认英文，详见 README「Language selection」）。
> This document is bilingual for readability only; the tool's runtime output language is user-controlled via `--lang` (default English — see README "Language selection").

The content is transcribed from [github/codeql](https://github.com/github/codeql)
(MIT License — see the attribution at the end):

内容逐字摘自 [github/codeql](https://github.com/github/codeql)（MIT License，见文末署名）：

| Upstream file / 来源文件 | What it provides / 提供什么 |
| --- | --- |
| `shared/concepts/codeql/concepts/internal/SensitiveDataHeuristics.qll` | the name regexes (`maybeSecret` etc.) and the exclusion regex (`notSensitiveRegexp`)<br>名字正则与反向排除器 |
| `python/ql/lib/semmle/python/dataflow/new/SensitiveDataSources.qll` | the 7 source classes<br>7 个 source 类 |
| `python/ql/lib/semmle/python/security/dataflow/CleartextStorageCustomizations.qll` | which sources CWE-312 takes, and what its sink is<br>CWE-312 取哪些 source、sink 是什么 |

> This document only explains **why a false positive happens**. Do **not** use it to close real alerts —
> look at the data flow printed by `scripts/read_sarif.py` first.
>
> 本文只解释「为什么会误报」。**不要**据此去关闭真实告警——先看 `scripts/read_sarif.py` 打出的数据流。

---

## 1. The decision input is the name, not the content / 判定入口：名字，而不是内容

Every source in `SensitiveDataSources.qll` requires the name to match a heuristic such as
`maybeSecret()` / `maybePrivate()`. They **never look at the value inside the variable**. So:

`SensitiveDataSources.qll` 里所有 source 都要求名字命中 `maybeSecret()` / `maybePrivate()` 等启发式。
它们**完全不看变量里装的是什么值**。所以：

```python
# Sample code / 示例代码 —— placeholder patterns, no credential involved
SECRET_PATTERNS = ["sk-[A-Za-z0-9]{20,}"]        # name matches  -> treated as sensitive data
CREDENTIAL_PATTERNS = ["sk-[A-Za-z0-9]{20,}"]    # renamed       -> no longer sensitive, logic unchanged
```

（中文：`SECRET_PATTERNS` 里只是一串正则，但名字命中了就被当敏感数据；换个名字就不再敏感，逻辑零变更。）

## 2. Five groups and their regexes / 五组分类与对应正则

### `maybeSecret()` → classification `secret`

```text
(?is).*((?<!is|is_)secret|(?<!un|un_|is|is_)trusted(?!_iter)|confidential).*
```

- Matches / 命中：`SECRET_PATTERNS`, `secret_key`, `my_secret`, `confidential_data`
- Does not match / 不命中：`is_secret` / `is_secret_…` (prefixes `is`, `is_` are excluded),
  `untrusted` / `un_trusted` / `untrusted_iter`
- Note: a name can match more than one group — `oauth_secret` classifies as
  `['secret', 'password']`, because `oauth` hits `maybePassword()` too. Compare those results with the
  `hits` list a prefilter run prints.
  注意：一个名字可以同时命中多组——`oauth_secret` 的分类是 `['secret', 'password']`
  （`oauth` 也命中 `maybePassword()`）。拿它和预筛脚本打印的 `hits` 对照着看。
- Easy to trip over: a `secret` substring anywhere is enough — **the word in front of it grants no
  exemption**, unless it is exactly `is` / `is_`
  容易踩：变量里只要含 `secret` 子串就够——**它前面的词不构成豁免**，除非正好是 `is` / `is_`

### `maybePassword()` → classification `password`

```text
(?is).*(pass(wd|word|code|.?phrase)(?!.*question)|(auth(entication|ori[sz]ation)?).?key|oauth|api.?(key|tok)|([_-]|\b)mfa([_-]|\b)).*
```

- Matches / 命中：`api_key`, `api_token`, `oauth_client`, `mfa_code`, `auth_key`
- Both `passphrase` and `pass_phrase` count; but a following `question` (`passphrase_question`) is
  excluded
  注意 `passphrase` / `pass_phrase` 都算；但后面跟 `question`（`passphrase_question`）会被排除

### `maybeAccountInfo()` → classification `id`

```text
(?is).*(acc(ou)?nt|puid|user.?(name|id)|session.?(id|key)).*
(?s).*([uU]|^|_|[a-z](?=U))([uU][iI][dD]).*
```

- Matches / 命中：`account_id`, `username`, `user_id`, `session_key`, `uid`, `customerUid`

### `maybeCertificate()` → classification `certificate`

```text
(?is).*(cert)(?!.*(format|name|ification)).*
```

- Matches / 命中：`client_cert`, `cert_pem`
- Excluded / 排除：anything containing `cert_format` / `cert_name` / `certification`
  含 `cert_format` / `cert_name` / `certification` 的不算

### `maybePrivate()` → classification `private`

Credit cards, national IDs / passports, addresses, phone numbers, biometrics, medical data,
`employer`, `mac_addr` and a long list of others. The full regex is the 5th group of the `MAYBE`
constant in `scripts/scan_sensitive_sources.py`.

信用卡、身份证/护照、住址、电话、生物特征、医疗、`employer`、`mac_addr` 等一长串。
完整正则见 `scripts/scan_sensitive_sources.py` 里 `MAYBE` 常量的第 5 组（`private`）。

## 3. The exclusion regex `notSensitiveRegexp()` / 反向排除器

Even if a name matches the regexes above, it is **not** sensitive as long as it also matches this one:

即使命中上面的正则，只要还命中下面这条就**不算**敏感：

```text
(?is).*([^\w$.-]|redact|censor|obfuscate|hash|md5|sha|random|(?<!unen)crypt|(?<!un)encode|certain|concert|secretar|wildcard|coauthor|account(ant|ab|ing|ed)|(?<!pro)file|path|([_-]|\b)url).*
```

What this means in practice (important) / 实践含义（很重要）：

- **`"[REDACTED_SECRET]"` is not treated as sensitive** — `redact` is in the exclusion list.
  So redacting a sensitive field is a valid fix; **do not go hunting for placeholders as a source**.
  **`"[REDACTED_SECRET]"` 不会被判敏感**——`redact` 在排除表里。
  所以「把敏感字段脱敏成 `[REDACTED_SECRET]`」是有效修复，**别把它当成污染源去查**。
- Names containing `file` / `path` / `url` / `hash` / `md5` / `encode` are usually ruled out
  immediately. Verified examples: `hash_id`, `path_id`, `url_id`, `encoded_blob` → all clean.
  (`profile` is the exception: `(?<!pro)file` means a `file` preceded by `pro` does not trigger the
  exclusion — and indeed `profile` stays clean for other reasons.)
  名字里带 `file` / `path` / `url` / `hash` / `md5` / `encode` 的通常直接出局
  （实测：`hash_id`、`path_id`、`url_id`、`encoded_blob` 全部干净）；
  `file` 前面是 `pro` 时不算触发排除（`(?<!pro)file`）。
- Substring matches that are **not words** are handled by word boundaries inside the patterns, e.g.
  `([_-]|\b)ssn([_-]|\b)`. Verified: `ssn`, `my_ssn`, `class_ssn` → `private`, while `classname` and
  `assembly_line` (which literally contain `ssn`) → clean. **When you port these regexes to another
  language, keep the word boundaries** or you will get false hits on ordinary words.
  靠 `([_-]|\b)ssn([_-]|\b)` 里的**词边界**处理的「含子串但不是词」的情况：
  实测 `ssn` / `my_ssn` / `class_ssn` → `private`，而字面含 `ssn` 的 `classname` / `assembly_line` → 干净。
  **移植到其它语言时务必保留词边界**，否则会误伤普通单词。
- The exclusion list also covers common words that merely contain a scary substring: `secretary`
  (`secretar`), `accountant` (`account(ant|…)`), `concert_id` (`concert`), `certainty`, `wildcard_hit`,
  `coauthor_list` → all verified clean.
  排除表还覆盖了一批「只是含敏感子串的普通词」：`secretary`（`secretar`）、`accountant`、
  `concert_id`、`certainty`、`wildcard_hit`、`coauthor_list` —— 实测均干净。

## 4. The seven source classes / 七类 source（`SensitiveDataSources.qll`）

| Class / 类 | Shape / 形态 |
| --- | --- |
| `SensitiveVariableAssignment` | `SECRET = ...` (including `for x in ...` loop variables and `with ... as x`)<br>`SECRET = ...`（含循环变量、`with ... as x`） |
| `SensitiveAttributeAccess` | `obj.api_key` |
| `SensitiveSubscript` | `d["api_key"]` |
| `SensitiveGetCall` | `d.get("api_key")` |
| `SensitiveParameter` | `def f(api_key)` |
| `SensitiveFunctionCall` | `get_secret()` |
| `GetPassCall` | `getpass.getpass()` |

## 5. `py/clear-text-storage-sensitive-data` (CWE-312) special cases
## 5. CWE-312 查询的特例

**The sources are filtered a second time** — `CleartextStorageCustomizations.qll`:

**source 会再筛一次**——`CleartextStorageCustomizations.qll`：

```ql
class SensitiveDataSourceAsSource extends Source, SensitiveDataSource {
  SensitiveDataSourceAsSource() {
    not SensitiveDataSource.super.getClassification() in [
        SensitiveDataClassification::id(), SensitiveDataClassification::certificate()
      ]
  }
  ...
}
```

⇒ For **this query**, only `secret` / `password` / `private` can fire; `id` (`user_id`,
`session_key`, …) and `certificate` are **explicitly excluded**.

⇒ 对**这条查询**而言，只有 `secret` / `password` / `private` 会引爆，
`id`（`user_id`、`session_key`…）与 `certificate` **被显式排除**。

**The sink is "data written to a file" / sink 是「写入文件的数据」：**

```ql
class FileWriteDataAsSink extends Sink {
  FileWriteDataAsSink() {
    this = any(FileSystemWriteAccess write).getADataNode() and ...
```

i.e. `Path.write_text` / `write_bytes`, `open(...).write(...)` and friends. The upstream source
carves out `pathlib.py` itself (to avoid reporting twice between `Path.write_bytes` and the internal
`f.write`).

即 `Path.write_text` / `write_bytes`、`open(...).write(...)` 之类。源码里对 `pathlib.py` 自身做了
carve-out（避免在 `Path.write_bytes` 与内部 `f.write` 之间重复报两条）。

So the complete trigger chain is / 所以完整触发链是：

```text
sensitive-name assignment → propagates through loop variable / dict / f-string → json.dumps or str concat → written to a file
敏感名赋值           → 沿循环变量/字典/f-string 传播 → json.dumps / str 拼接 → 写入文件
```

## 6. How to fix it / 修复取向

| Approach / 做法 | Verdict / 评价 |
| --- | --- |
| **Rename** (`SECRET_PATTERNS` → `CREDENTIAL_PATTERNS`)<br>**改名** | ✅ Preferred. Zero behavioural change, no change to the data flow, no public API moved.<br>✅ 首选。逻辑零变更，不动数据流，不改公共接口 |
| Actually redact the field (`[REDACTED_SECRET]`)<br>把字段真的脱敏 | ✅ Effective, and `redact` is in the exclusion list.<br>✅ 有效，且 `redact` 在排除表里 |
| `# lgtm` / `# codeql[...]` suppression comments<br>抑制注释 | ⚠️ Hides the conclusion; the next reader still has to investigate it again.<br>⚠️ 藏住了结论，下一个人仍要重查一遍 |
| Dismissing the alert on GitHub<br>在 GitHub 上 dismiss | ⚠️ Last resort. A false positive needs a written justification; **if a rename fixes it, do not dismiss**.<br>⚠️ 最后手段。误报要写清理由；**改名能解决的就别 dismiss** |

Afterwards, leave a comment at the definition saying **"do not rename this back"** plus the rule that
caused it — otherwise the next person will helpfully revert it.

改完记得在源码里留一句「**勿改回去** + 规则出处」，否则下一个人会顺手把名字改回来。

---

## Attribution / 署名

The regexes and QL snippets in this document come from [github/codeql](https://github.com/github/codeql),
Copyright GitHub, Inc., licensed under the MIT License. This document and this repository's
`scripts/scan_sensitive_sources.py` are readable restatements / equivalent ports of those definitions,
not official GitHub artifacts.

本文的正则与 QL 代码片段取自 [github/codeql](https://github.com/github/codeql)，
Copyright GitHub, Inc.，以 MIT License 授权。本文档与本仓库的 `scripts/scan_sensitive_sources.py`
均为对这些定义的可读重述/等价移植，不是 GitHub 官方产物。
