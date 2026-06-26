## 概览

ai-shifu-course-creator 是一个把"原始素材 → 可运行的 MarkdownFlow 课程脚本 → AI-Shifu 平台上线课程"全流程封装起来的 skill。整体由四类组件构成：

- 主入口规则文件：[SKILL.md](../SKILL.md)
- 唯一对外执行器：[scripts/shifu-cli.py](../scripts/shifu-cli.py)
- 规则与契约（references/）
- 用法示例（examples/）

下文用三张 mermaid 图分别呈现：① skill 整体架构；② 全流程及中间产物；③ 文件之间的对应关系。

## 1. Skill 整体架构

```mermaid
graph TB
    subgraph SKILL["ai-shifu-course-creator/"]
        direction TB
        SkillMd["SKILL.md<br/>主入口 / 规则与流程总纲"]

        subgraph Scripts["scripts/"]
            CLI["shifu-cli.py<br/>唯一对外执行器<br/>build / import / publish / show ..."]
        end

        subgraph References["references/ — 规则与契约（按用途与关注点分组）"]
            R1["markdownflow.md<br/>语法 + preservation + deterministic 块<br/>（违反 → 跑不动）"]
            R2["pedagogy.md<br/>教学法 + 教学约束<br/>（违反 → 教学差）"]
            R3["data-contracts.md<br/>input + output + language + lesson schema"]
            R4["course-prompt.md<br/>课程级提示词 rules + template"]
            R5["review-checklist.md<br/>Optimization 阶段全面审计清单"]
            R6["report-template.md<br/>报告模板（用户面向）"]
            subgraph CliRefs["cli/ — 工程契约（scripts 消费）"]
                R7["cli-reference.md<br/>CLI 命令手册"]
                R8["course-directory-spec.md<br/>课程目录约定"]
                R9["import-json-format.md<br/>导入 JSON 协议"]
            end
        end

        subgraph Examples["examples/"]
            E1["pipeline-full.md"]
            E2["segmentation-only.md"]
            E3["generation-only.md"]
            E4["optimization-only.md"]
            E5["fallback-mode.md"]
            E6["end-to-end-deploy.md"]
            E7["deploy-only.md"]
        end

        subgraph Other["design/ + evals/"]
            D1["design/todo.md<br/>trigger_eval_process.md"]
            D2["evals/<br/>触发 / 行为评测样例"]
        end

        Env[".env<br/>登录态 token"]
    end

    SkillMd -->|引用| References
    SkillMd -->|展示用法| Examples
    SkillMd -->|调用| CLI
    CLI -->|读写| Env
    CLI -->|遵循协议| R7
    CLI -->|遵循协议| R8
    CLI -->|按手册定义| R9

    classDef entry fill:#fff4d6,stroke:#caa42a,color:#222
    classDef code fill:#e3f2fd,stroke:#1565c0,color:#222
    classDef ref fill:#f1f8e9,stroke:#558b2f,color:#222
    classDef ex fill:#fce4ec,stroke:#ad1457,color:#222
    classDef misc fill:#eee,stroke:#666,color:#222

    class SkillMd entry
    class CLI,Env code
    class R1,R2,R3,R4,R5,R6,R7,R8,R9 ref
    class E1,E2,E3,E4,E5,E6,E7 ex
    class D1,D2 misc
```

## 2. 从建课到发布的全流程 + 中间产物

```mermaid
flowchart TB
    Raw["原始素材<br/>讲稿 / 大纲 / 笔记 / PDF"]:::input

    subgraph P1["Segmentation 切分"]
        P1Work["清洗 → 标记不可变块<br/>语义切分 → 课时候选"]
    end
    Seg["有序 segments 列表<br/>+ 课时边界候选<br/>+ 每课 core_question<br/>+ preservation index<br/>+ transfer-signal 包<br/>（中间结构，内存对象）"]:::mid

    subgraph P2["Orchestration 编排（元层）"]
        P2Work["归并 / 排序素材<br/>调度 P1 与 P3<br/>跑 mandatory gates"]
    end
    CIdx["course_index<br/>（lesson_id / title / core_question / source_span）"]:::mid
    GVar["global_variable_table<br/>（name / collected_in / used_in / scope）"]:::mid

    subgraph P3["Generation 生成"]
        P3Work["按 data-contracts.md#lesson-schema 生成<br/>每课 Teaching Prompt（用 MarkdownFlow 书写）<br/>遵循 pedagogy.md（teaching patterns）"]
    end
    LessonsDraft["lesson_teaching_prompts<br/>（每课一个 Teaching Prompt 草稿）"]:::mid

    subgraph P4["Optimization 审计优化"]
        P4Work["coverage 矩阵<br/>按 issue class 打标<br/>最小安全编辑<br/>review-checklist 复核"]
    end
    LessonsOpt["优化后 Teaching Prompts<br/>+ Course Prompt<br/>+ 审计报告（按 report-template）"]:::mid

    subgraph P5["Deployment 部署"]
        direction TB
        Dir["course directory（落盘）<br/>README.md / course-prompt.md<br/>lessons/lesson-*.md<br/>structure.json (可选)"]:::file
        Build["shifu-cli.py build<br/>（离线打包）"]
        Json["shifu-import.json<br/>（导入协议产物）"]:::file
        Imp["shifu-cli.py import --new"]
        Pub["shifu-cli.py publish &lt;shifu_bid&gt;"]
    end

    Live["AI-Shifu 平台上线课程<br/>shifu_bid + preview URL"]:::output

    Raw --> P1Work --> Seg
    Seg --> P2Work
    P2Work --> CIdx
    P2Work --> GVar
    P2Work --> P3Work
    P3Work --> LessonsDraft
    LessonsDraft --> P4Work
    CIdx --> P4Work
    GVar --> P4Work
    P4Work --> LessonsOpt

    LessonsOpt --> Dir
    CIdx -.结构信息.-> Dir
    GVar -.变量元数据.-> Dir
    Dir --> Build --> Json --> Imp --> Pub --> Live

    %% 旁路：单独入口
    RawScripts["已有 Teaching Prompts + Course Prompt<br/>（Path C 直接部署）"]:::input
    RawScripts --> Dir

    ExistingCourse["已上线课程<br/>（Path D 管理）"]:::input
    ExistingCourse -.list / show / update-lesson<br/>rename / reorder / archive.-> Live

    classDef input fill:#fff4d6,stroke:#caa42a,color:#222
    classDef mid fill:#e3f2fd,stroke:#1565c0,color:#222
    classDef file fill:#f3e5f5,stroke:#6a1b9a,color:#222
    classDef output fill:#c8e6c9,stroke:#2e7d32,color:#222
```

## 3. 中间文件与产物的对应关系

```mermaid
flowchart LR
    subgraph SRC["素材层"]
        Raw["原始素材<br/>（任意格式）"]
    end

    subgraph LOGIC["逻辑产物（Segmentation–Optimization，Output Contract 定义）"]
        Seg["segments + transfer signals"]
        Idx["course_index"]
        Var["global_variable_table"]
        Mdf["lesson_teaching_prompts<br/>（每课一份 Teaching Prompt）"]
        Sys["Course Prompt<br/>（AI 角色 / 教学风格 / 写作 / 视觉 / 翻译）"]
    end

    subgraph DISK["落盘文件（course directory）"]
        Readme["README.md<br/>（标题 = 课程名）"]
        SysFile["course-prompt.md"]
        StructFile["structure.json<br/>（多章可选）"]
        LessonFiles["lessons/lesson-01.md<br/>lessons/lesson-02.md<br/>..."]
    end

    subgraph BUILD["构建产物"]
        ImportJson["shifu-import.json<br/>{ shifu, outline_items, structure }<br/>shifu.course_prompt"]
    end

    subgraph PLATFORM["AI-Shifu 平台对象"]
        Shifu["shifu（课程）<br/>shifu_bid"]
        Outline["outline_items<br/>章 (parent_bid='') / 课 (type=401)"]
        URL["preview / live URL"]
    end

    Raw --> Seg
    Seg --> Idx
    Seg --> Var
    Seg --> Mdf

    Idx -- "决定章节顺序" --> StructFile
    Idx -- "lesson_title / 顺序" --> LessonFiles
    Var -- "变量在 Teaching Prompt 中落地为 %{{var}}" --> LessonFiles
    Mdf -- "每条 teaching_prompt → 一个 .md" --> LessonFiles
    Sys -- "落盘" --> SysFile
    Idx -- "课程标题 → 第一个 H1" --> Readme

    Readme -- "title → shifu.title" --> ImportJson
    SysFile -- "→ shifu.course_prompt" --> ImportJson
    StructFile -- "→ outline_items 章节树" --> ImportJson
    LessonFiles -- "正文 → outline_items[].content" --> ImportJson

    ImportJson -- "import --new<br/>course_prompt → API system_prompt" --> Shifu
    ImportJson -- "outline_items" --> Outline
    Shifu --> URL
    Outline --> URL

    classDef input fill:#fff4d6,stroke:#caa42a,color:#222
    classDef logic fill:#e3f2fd,stroke:#1565c0,color:#222
    classDef file fill:#f3e5f5,stroke:#6a1b9a,color:#222
    classDef build fill:#ffe0b2,stroke:#ef6c00,color:#222
    classDef plat fill:#c8e6c9,stroke:#2e7d32,color:#222

    class Raw input
    class Seg,Idx,Var,Mdf,Sys logic
    class Readme,SysFile,StructFile,LessonFiles file
    class ImportJson build
    class Shifu,Outline,URL plat
```

## 关键说明

- **逻辑产物 vs 落盘文件**：Segmentation–Optimization 的 `segments / course_index / global_variable_table / lesson_teaching_prompts / course_prompt` 由 [data-contracts.md#output-contract](../references/data-contracts.md#output-contract) 定义，是会话内的逻辑对象；只有进入 Deployment 时才按 [cli/course-directory-spec.md](../references/cli/course-directory-spec.md) 写入 `README.md` / `course-prompt.md`（Course Prompt）/ `lessons/lesson-*.md`（每课一份 Teaching Prompt）/ `structure.json`。
- **唯一执行器**：所有平台交互都走 [shifu-cli.py](../scripts/shifu-cli.py)（`build / import / publish / show / update-lesson` 等），SKILL 明确禁止直接调 HTTP API。
- **build 是离线步骤**：把课程目录打包成 [shifu-import.json](../references/cli/import-json-format.md)（`shifu` + `outline_items` + `structure`），然后由 `import --new` 或 `import <bid>` 推送到平台，最终 `publish` 上线。
- **Course Prompt 命名映射（CLI 内部）**：本仓库对外统一叫 `course_prompt`（文件名 `course-prompt.md`、JSON 字段 `shifu.course_prompt`、CLI 参数 `--course-prompt-file`）；CLI 在调 `/shifus/<bid>/detail` 时会把它映射成平台 API 的 `system_prompt` 字段。
- **四种使用路径**：
  - Path A — 全流程（Orchestration → Optimization → Deployment）；
  - Path B — 只产 MarkdownFlow（Segmentation–Optimization，不部署）；
  - Path C — 已有脚本直接部署（仅 Deployment）；
  - Path D — 管理已上线课程（list / update / rename / reorder / archive 等）。

## 4. shifu-cli.py 提供的接口能力

所有平台交互都通过 [scripts/shifu-cli.py](../scripts/shifu-cli.py) 完成。CLI 共有 17 个子命令，按职能分为六组。详细参数见 [cli-reference.md](../references/cli/cli-reference.md)。

### 4.1 命令总览（按职能分组）

| 分组 | 命令 | 作用 | 是否联网 |
|---|---|---|---|
| 认证 | `login` | 手机号 + 4 位短信验证码登录，token 写入 `.env` | ✅ |
| 查询 | `list` | 列出当前账号下所有课程 | ✅ |
| 查询 | `show <shifu_bid> [outline_bid]` | 查看课程大纲树；带 outline_bid 时读取该课的 MarkdownFlow 正文 | ✅ |
| 查询 | `history <shifu_bid> <outline_bid>` | 查看一课的 Teaching Prompt 修订历史 | ✅ |
| 查询 | `export <shifu_bid> [-o file.json]` | 把课程导出为 JSON | ✅ |
| 创建 | `create --name ... [--description ...]` | 创建空课程（仅 shifu 主体，无章节） | ✅ |
| 创建 | `add-chapter <shifu_bid> --name ...` | 新增一个顶层章节 | ✅ |
| 创建 | `add-lesson <shifu_bid> --name ... --parent-bid ... [--teaching-prompt-file ...]` | 在指定章节下新增一课，可附带 Teaching Prompt 文件 | ✅ |
| 更新 | `update-meta <shifu_bid> [--name] [--description] [--course-prompt-file]` | 更新课程标题 / 简介 / Course Prompt | ✅ |
| 更新 | `update-lesson <shifu_bid> <outline_bid> --teaching-prompt-file ...` | 替换一课的 Teaching Prompt（带乐观锁） | ✅ |
| 更新 | `rename-lesson <shifu_bid> <outline_bid> --name ...` | 仅改课时名称 | ✅ |
| 更新 | `reorder <shifu_bid> --order bid1,bid2,bid3` | 按给定顺序重排课时 | ✅ |
| 删除 | `delete-lesson <shifu_bid> <outline_bid>` | 删除一课 | ✅ |
| 构建 / 导入 | `build --course-dir ... [-o ...] [--title] [--chapter-name] [--description] [--keywords]` | 离线把课程目录打包成 `shifu-import.json` | ❌ |
| 构建 / 导入 | `import --new --json-file ...` 或 `import --new --course-dir ...` | 用 JSON / 目录创建一门新课程 | ✅ |
| 构建 / 导入 | `import <shifu_bid> --json-file ...` 或 `import <shifu_bid> --course-dir ...` | 把 JSON / 目录覆盖到已有课程 | ✅ |
| 状态 | `publish <shifu_bid>` | 发布课程，对外可见 | ✅ |
| 状态 | `archive <shifu_bid>` / `unarchive <shifu_bid>` | 归档 / 取消归档 | ✅ |

### 4.2 命令调用图

```mermaid
flowchart LR
    User["Skill / 用户"]:::user

    subgraph CLI["shifu-cli.py"]
        direction TB
        Auth["login"]:::auth

        subgraph Read["查询类（只读）"]
            List["list"]
            Show["show"]
            Hist["history"]
            Exp["export"]
        end

        subgraph Write["写入类"]
            Create["create"]
            AddCh["add-chapter"]
            AddLs["add-lesson"]
            UpMeta["update-meta"]
            UpLs["update-lesson<br/>(乐观锁)"]
            Rn["rename-lesson"]
            Reord["reorder"]
            Del["delete-lesson"]
        end

        subgraph Bulk["批量构建 / 导入"]
            Build["build<br/>（离线）"]
            Imp["import<br/>(--new / &lt;bid&gt;)"]
        end

        subgraph State["生命周期"]
            Pub["publish"]
            Arch["archive"]
            Unarch["unarchive"]
        end
    end

    Env[".env<br/>token"]:::env
    Platform["AI-Shifu 平台 API<br/>https://app.ai-shifu.cn"]:::plat
    LocalDir["本地课程目录"]:::file
    LocalJson["shifu-import.json"]:::file

    User --> Auth --> Env
    User --> Read
    User --> Write
    User --> Bulk
    User --> State

    Env -. 注入 token .-> Read
    Env -. 注入 token .-> Write
    Env -. 注入 token .-> Bulk
    Env -. 注入 token .-> State

    LocalDir --> Build --> LocalJson --> Imp
    LocalDir -. 一步式 --course-dir .-> Imp

    Read -->|HTTP| Platform
    Write -->|HTTP| Platform
    Imp -->|HTTP| Platform
    State -->|HTTP| Platform

    classDef user fill:#fff4d6,stroke:#caa42a,color:#222
    classDef auth fill:#ffe0b2,stroke:#ef6c00,color:#222
    classDef env fill:#eee,stroke:#666,color:#222
    classDef plat fill:#c8e6c9,stroke:#2e7d32,color:#222
    classDef file fill:#f3e5f5,stroke:#6a1b9a,color:#222
```

### 4.3 用法路径与命令映射

| 路径 | 典型命令序列 |
|---|---|
| **Path A 全流程** | （生成 lessons/ 后） → `build --course-dir ./course/` → `import --new --json-file ./course/shifu-import.json` → `publish <bid>` |
| **Path C 仅部署已有脚本** | 同上 build/import/publish |
| **Path D 管理已上线课程** | `list` / `show` / `update-meta` / `update-lesson` / `rename-lesson` / `reorder` / `delete-lesson` / `archive` / `unarchive` / `history` / `export` |
| **从零增量搭建** | `create` → `add-chapter` → `add-lesson`（重复） → `publish` |

### 4.4 关键设计点

- **唯一入口**：所有平台交互都走 CLI，SKILL.md 明确禁止直接调原始 HTTP API。
- **离线 / 在线分离**：`build` 是纯本地操作（不联网），其他命令需要 token；这种分离方便在 CI / 受限网络下先打包再分发。
- **两种导入形态**：`import --json-file` 接受预先 build 好的 JSON；`import --course-dir` 在内部先 build 再 import，等价于一键发布。
- **两种创建模式**：`import --new` 用于完整目录一次建课；`create + add-chapter + add-lesson` 用于细粒度逐步搭建。
- **乐观锁**：`update-lesson` 会先拉取当前 revision，若服务端已被他人修改则拒绝写入，避免覆盖他人改动。
- **token 持久化**：`login` 把 token 写到 `.env`，后续命令无需重复登录；token 失效时再次跑 `login` 即可。
