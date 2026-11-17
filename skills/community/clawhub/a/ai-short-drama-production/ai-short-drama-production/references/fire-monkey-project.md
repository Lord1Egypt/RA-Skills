# Fire Monkey / Flame Advertising Project

> Optional case study. The generic workflow must remain usable with a different IP, character set, studio, language, and model vendor.

## Project identity

- Character prototype: 火花猴 / Fire Monkey
- Copyright owner: 火焰广告
- Copyright line: `© 2026 火焰广告 版权所有`
- Default language: Chinese
- Format: vertical animated AI short drama, `9:16`, `720×1280` test, `1080×1920` final, `24 fps`
- Current season: three 20-episode series, about 120 seconds per episode

## Series

1. 民生热点：《火花猴·有事找猴哥》
2. 国学成长：《火花猴·文心奇旅》
3. 玄幻热血：《火花猴：烬火行者》

## Canonical source files

- Refined scripts and correction log:
  `C:\Users\ASUS\Documents\Codex\2026-11-05\new-chat\outputs\火花猴AI短剧三套剧本_V2_精修版`
- Episode 1 Seedance package:
  `C:\Users\ASUS\Documents\Codex\2026-11-05\new-chat\outputs\火花猴_Seedance第1集制作包`
- E-drive production master:
  `E:\seedance\火猴\AI短剧制作总盘`
- E-drive script and trailer packages:
  `E:\seedance\火猴\剧本`
- Character assets:
  `E:\seedance\火猴\火花猴`

## Character consistency lock

Base references used for the three tests:

- primary: `E:\seedance\火猴\火花猴\1.1.png`
- face: `E:\seedance\火猴\火花猴\头像\微信图片_20261111143641_755_2.png`

Base anchor:

`火花猴，橙金短毛、圆耳、大眼、额前火焰形呆毛、火焰长尾，儿童比例；脸型、耳朵、眼睛、尾巴形状和体型绝不改变，只更换服装和世界观。`

Outfits:

- 民生：黄色社区志愿者马甲、火焰徽章、斜挎包、手机稳定器；
- 国学：墨色小书童短褂、朱红束带、腰侧毛笔、宣纸纹衣摆；
- 玄幻：赭红短甲、铜色护腕、腰间煤坠；吸冷火后尾巴出现蓝纹。

## Verified model and API

- model: `doubao-seedance-2-5-260628`
- create task: `POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`
- auth: environment variable `ARK_API_KEY`
- duration: 4–30 seconds
- test resolution: `720p`
- final resolution: `1080p`
- audio: `generate_audio:false` for dialogue-first episodes; `true` for non-dialogue trailer tests
- watermarks and final Chinese text: add in post

## Test trailers completed

All are 30 seconds, `720×1280`, `24 fps`, H.264/AAC, with Flame Advertising copyright watermark and metadata.

- 玄幻: task `cgt-20261112095741-mt1yo`
- 民生: task `cgt-20261112102454-1am3c`
- 国学: task `cgt-20261112102457-15oy3`

Completed files:

- `玄幻预告片_30s_720p_火焰广告版权版.mp4`
- `民生预告片_30s_720p_火焰广告版权版.mp4`
- `国学预告片_30s_720p_火焰广告版权版.mp4`
- `三版火猴角色一致性对照.jpg`
- `版权声明_火焰广告.txt`
- `版权登记信息_火焰广告.json`

## Script quality standard (v1.1)

- Each scene must have objective, obstacle, tactic, turn, and exit.
- Every episode must change knowledge, power, relationship, safety, ownership, identity, or moral position.
- Cliffhanger types must rotate and inherit the previous episode's unresolved pressure.
- Coverage must preserve eyelines, screen direction, prop hand, light direction, and scene geography.
- Every camera move must have a narrative intention.
- Prompt blocks must specify one dominant action and one dominant camera idea per 4–8 seconds.
- Voice performance must specify objective, tactic, beat, emphasis, pause, and visible/off-screen state.
- Dialogue and lip-sync are timed from final voice, not from auto-generated model audio.

## Current production rules

- Every episode has about 15 shots and 120 seconds.
- Each shot must have a timecode, duration, action, prompt, character IDs, dialogue/SFX, and status.
- Use the same character references and outfit ID per series.
- Use one 30-second generation task only when the shot plan is intentionally multi-shot; otherwise generate per shot.
- All signs, phone UI, contracts, newspaper, scroll text, and subtitles are post-produced.
- Keep raw takes and copyright masters separately.
- Any new paid batch requires explicit approval after reporting task count, resolution, duration, and expected wait.

## Cinematic technique standard (v1.2)

- Each episode selects one primary storytelling technique, one staging technique, one transition family, one hero VFX motif, and one recurring visual or sound gag.
- 民生剧 can use underdog comedy, prop-driven evidence gags, and ironic montage.
- 国学剧 can use visual rhymes, quiet observation, ink transitions, and object-based memory.
- 玄幻剧 can use ensemble standoffs, static wide geography, sudden bursts of action, and elemental VFX punctuation.
- Named filmmaker references are craft studies only; do not copy recognizable scenes, costumes, dialogue, music, or shot sequences.

## Workload baseline

Using 60 episodes × 120 seconds × 15 shots, 2.5 variants, 15% rework, 12 characters, 30 scenes, and medium complexity:

- accepted shots: 900
- keyframes: 1,080
- raw generations: 2,588
- estimated storage: 128.7 GB
- estimated person-hours: 1,088.1
- estimated person-days: 136.0
- generation wall time at 4 parallel tasks: 86.3 hours
- estimated calendar duration with a five-person team: 34.9 days

A three-episode cross-series pilot estimates to:

- accepted shots: 45
- raw generations: 130
- person-hours: 96.1
- estimated calendar duration with a four-person team: 3.6 days

These are planning baselines, not vendor quotes. Actual time depends on retry rates, character consistency, voice recording, and approval speed.

## Next production step

The pilot trailers are complete. The next efficient step is:

1. Approve the Fire Monkey continuity from `三版火猴角色一致性对照.jpg`.
2. Choose one series for a three-episode pilot.
3. Generate Episode 1 per shot from `04_Seedance逐镜头任务清单.jsonl`.
4. Add voice, subtitles, lip-sync, post text, and copyright.
5. Review retention and cost before scaling to 20 episodes.
