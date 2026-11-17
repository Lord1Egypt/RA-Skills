# Audio/video backtest evidence

**Question tested:** can this pipeline take a public 业绩会 **audio/video** source through `parse → omni-source → build → update → validate → verbatim re-check → export-okf`, well enough to support 「含音视频」 in the package's name/summary?

**Answer as measured: YES for local bounded clips (inside the tool's 256 MiB source limit) — public earnings-meeting video clips from **two independent meetings** completed the full chain with 8/8 verbatim re-check hits (3 parsed clips, 3 sources, 8 packaged facts). NO for full-length meetings: every full-video attempt (URL leg, both CDNs; local leg, size gate) failed.** The claim is therefore **supported with a stated workflow bound (local split ≤256 MiB)**, not unsupported; and full-length direct-URL AV parsing remains 未臻.

## Layers of evidence (machine facts are recorded in the internal run ledger, available on request)

这里的 L1–L4 是**回测腿档**（本文件是这套字母在本仓的唯一定义处，别包不引用它）：L1＝URL 侧整片可读性，L2＝本地整档字节一致，L3＝本地有界片段进解析链，L4＝在 L3 的产物上跑完整链。它与本仓另外几包里用作**来源可信级**的 L1/L2/L3 无关——那三级指来源（域直查／用户直供／深研二手），不是腿档。

| Layer | What | Result |
|---|---|---|
| L1 URL leg, full videos | 3 public full meetings: 当升 2025H1 回放 (86 MB, h264+aac, 374 s, newscdn CDN), 建行 2025年度 (1.34 GB, 5866 s), 建行 2026H1 (1.34 GB, 5265 s, vod.ccb.cn). Legs: remote `detail=text` (lead ×3) + this path `detail=grounded` (×2) | **all PARSE_FAILED**: `failure_scope=parser, retryable=false, operation_created=true, parser_started=true, billed=false, content_released=false`. Generic message, no per-cause signal; unchanged retries not attempted (per schema) |
| L2 local leg, full file | 建行 H1 downloaded byte-exact (1,406,940,817 B = Content-Length; ffprobe h264+aac verified) | **SOURCE_TOO_LARGE**: `failure_scope=source, constraints.max_bytes=268435456 (256 MiB), operation_created=false, file_uploaded=false, billed=false` — a clean documented pre-parser gate, not a parser failure |
| L3 local leg, bounded clips | 3 clips cut+re-encoded locally: 建行 H1 ×2 （90 s each; 3.2 MB @t=600 s slide-画面段， 6.3 MB @t=2400 s 行长口播段） + 当升 2025H1 ×1 （4.0 MB, 90 s 口播开场段， downloaded byte-exact 90,128,405 B） — faststart h264+aac | **all 3 COMPLETED**, `detail=grounded`, `kind=bundle` (`omni.result_bundle.v1`): content.md (3298/1888/… B) + `grounding.data` sidecar (`omni.grounding.v1`, segments with time anchors). Returned shape uses inline anchors `[画面 mm:ss]` / `[说话人0 mm:ss]`, slide titles marked `(幻灯片标题)` |
| L4 full chain on L3 output | `omni-source --text-only --parse-origin omni_live` (source url = upstream public mp4 URL, honest derivation note in title) → `prepare` (verbatim quotes → byte spans) → `build` v1 (4 slide claims) → `update` v2 （+1 口播 claim, 2nd source; same scope title 增量） → `update` v3 （+3 当升口播中文读数 claims, 3rd source, 2nd entity） → `validate` ok → independent verbatim re-check (recomputed sha of every evidence span against source bytes) → `query --with-evidence` → `export-okf` | **chain complete on 2 independent meetings**: package = 3 sources / 8 assertions / 8 facts; verbatim re-check **8/8 HIT**; query returns `found` with evidence; export = 8 concept files + index; `run.json.skill_version = 0.3.2` (the three-place version lock now self-evidences on AV output) |

## Extracted-content examples (what a consumer gets)

- 画面 (slide) source: 「投向制造业的贷款余额4.15万亿元，增长17.95%」「民营企业贷款余额7.36万亿元，增长9.42%」「涉农贷款增长4.96%」「个人消费贷款余额8,068亿元，增长14.59%」
- 口播 (speech) source, ASR as returned, homophones NOT corrected (kept verbatim, declared in basis): 「二季度当季的**利用**是百分之一点三八，较一季度回升了两个基点。」— 利用 = 净息差 ASR mis-hear; a consumer of the knowledge pack sees the raw quote plus the note in the fact basis.

## Limits (per line, no rounding up)

- Sample: 3 full videos across 2 CDNs, all full-length parse attempts failed; 3 successful parses are **90-second fragments spanning two independent meetings （建行 H1 发布会 ×2 段、当升 2025H1 说明会 ×1 段）**. N for end-to-end = 2 meetings — small, and each meeting is represented by one time-window, not its whole arc.
- Local-leg preprocessing: clips were cut and **re-encoded by ffmpeg on this machine** before parse; the parser consumed normalized small mp4 files. A raw (not re-encoded) small file, other codecs (hevc/opus), pure audio (mp3/m4a), and HLS `.m3u8` were not each isolated.
- The 256 MiB gate means a full 90-minute HD 业绩会 (1.3–1.4 GB) cannot pass the local leg whole; splitting is a workflow, but per-split stitching/timestamp continuity is **not established** here.
- URL-leg failures carry one generic parser message; cause (CDN auth/redirect, size, codec at ingest) is not attributed by the returned facts and is not guessed here.
- The companion 文字实录 page for the meeting parsed as a **navigation shell whose body is a PDF attachment** (4602 B, 0 numeric hits) — a G7b-class page-shape finding; transcript-vs-video cross-check therefore was not performed.
- Two failure classes deliberately kept separate: parser `PARSE_FAILED` (remote/URL) vs client `stdio transport cannot be reconnected` (this session's MCP handle before reload; never reached the provider, not a parse result).
- Billing: all failed parses returned `billed=false`. The two completed parses did not surface a billing field to this driver — actual charge, if any, stands with the provider/Owner account record; **no rate or amount is inferred here**.

## Lead cross-session reproduction (post Bridge 1.8.6 reload, 2026-10-08 05:08:25)

- Session: gtm:1.1 (separate Bridge process, audited 1.8.6 pin + allowed-root /data/sdc1/work/gtm applied per skill setup contract).
- URL leg, fresh operations after reload: dangsheng mp4 grounded -> PARSE_FAILED (new op id, retryable=false, billed=false); CCB ee60 grounded re-attach -> same cached failure fingerprint (re-attach semantics, not a new attempt).
- Local leg, bounded clip: inputs/ccb-h1-clip90.mp4 grounded -> **completed**; bundle omni.result_bundle.v1, grounding omni.grounding.v1 (format=video), [画面 mm:ss] + （幻灯片标题） + [说话人 mm:ss] anchors as described above; content digest sha256:2c60012d...; billed with credits consumed (expires_at present).
- Verdict unchanged and now two-session reproducible: audio/video works **as a bounded local-file workflow**; public full-length video URLs are not served by the parser on either Bridge session.

## What this decides

- 「含音视频」 in name/summary: **supportable only with the qualification 「本地小段/切片(≤256 MiB)工作流」**; measured strength = 「2 场公开业绩会视频共三枚 90 秒切片走通全链(build→update×2→validate→query→export-okf)、逐字回查 8/8(100%)，全长视频 URL 路 5 枪全拒吐、本地全长受 256 MiB 闸」. Full-length meeting parsing = 未臻. Recommendation to lead/4.1: if added, phrase the hook as capability-with-bound, not blanket 「任意音视频」.
- This record does not claim general extraction accuracy; the two clips' re-check hit is byte-verbatim matching of quotes against parser output, which is integrity, not semantic truth.

Machine transcript, package output and export are recorded in the internal run ledger (per-message JSON-RPC), available on request.
