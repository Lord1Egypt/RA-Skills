<!--
文件：SUBMISSION-CHECKLIST.md
核心功能：记录 DaE 技能在 ClawHub / OpenClaw 提交前的核对项，避免遗漏入口、文案、安全说明与演示资产。
输入：技能包结构、发布文案、GitHub 仓库与 benchmark 资产。
输出：一份可执行的提交前清单。
-->

# Submission Checklist

## Package

- `SKILL.md` exists and has YAML frontmatter
- skill name is `dae-persona-context-injector`
- prompt reference is linked
- acceptance reference is linked
- security statement is present

## Public assets

- public repository is live: `https://github.com/sirsws/dae-persona-context-injector`
- benchmark page is public
- benchmark profile is public
- ClawHub copy is ready

## Positioning

- English is the primary submission language
- headline remains `DaE: Persona Context Injector`
- one-line promise stays concrete, not academic
- product repo remains separate from the SSRN research repo

## Safety

- no private user profile is included
- no token or credential appears in the package
- no claim exceeds the actual behavior of the skill
- security notes explicitly state local/private handling expectations

## Suggested submission fields

- title: `DaE: Persona Context Injector`
- one-line description: `Generate a reusable PersonaProfile that downstream agents can read before planning, coding, writing, researching, or advising.`
- repo URL: `https://github.com/sirsws/dae-persona-context-injector`
- benchmark URL: `https://github.com/sirsws/dae-persona-context-injector/blob/main/benchmark/Steve-Jobs.md`
- security URL: `https://github.com/sirsws/dae-persona-context-injector/blob/main/skill/dae-persona-context-injector/SECURITY.md`

## After submission

- verify skill page renders the diff block correctly
- verify repo links are clickable
- record whether the platform labels the skill as safe / benign / suspicious
- if the platform flags anything, capture the exact wording before editing
