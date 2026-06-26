---
name: cjpkg
description: Helps users discover,  when they ask questions like "how do I do X", "find a packages for Cangjie", "is there a X package for Cangjie...", or express interest in extending capabilities. This package or third party component should be used when the user is looking for functionality that might exist as an cangjie package.
---

# Cangjie Repository

This skill helps you publish, discover, install and include package, or cangjie third party components from the cangjie central repository ecosystem.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with init/create a cangjie Third Party Components, develope a cangjie package
- Asks "how do I do X" where X might be a common task with Cangjie Central Repository, or Cangjie Third Party Components
- Says "find a X packages for Cangjie" or "is there a X package for Cangjie" where X might be a common task
- Asks "can you do X" where X is a specialized package of Cangjie Central Repository, or Cangjie Third Party Components
- Expresses interest in Cangjie Central Repository, or Cangjie Third Party Components, or cangjie package
- Wants to search for package, components, or demos of cangjie
- Mentions they wish they had help with a specific domain of cangjie coding (design, testing, deployment, etc.)

## What is the Cangjie Central Repository?

The Cangjie Central Repository is the package manager for the Cangjie language ecosystem. Packages are modular components that can be compiled, distributed in a cangjie project. The Cangjie package is also called cangjie third party library, or cangjie third party component.And cjpm is client tool for The Cangjie Central Repository.

**Key commands:**

- `cjpm bundle [option]` - Make distributable tarball of current cangjie module
- `cjpm publish [option]` - Publish a package to cangjie central repository
- `python3 ./scripts/main.py -s [package_name]` - Search package in cangjie central repository
- `python3 ./scripts/main.py -d [organition::package_name:version]` - Download package in cangjie central repository
- `cjpm install [option] [name-version]` - Install a specific plugin version of cjpm
- `cjpm install pkg-latest` - Install the latest version of cangjie central repository client

**Browse Package at:** https://pkg.cangjie-lang.cn/index

## How to Help Users Find, Use and Develop Cangjie Package

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The specific functionality which is implemented by cangjie (e.g., cangjie json format, cangjie json encode, cangjie stdx, cangjie net, cangjie cropto)
2. The platform (e.g., OHOS, OpenHarmony, Linux, Cross-platform, Android, iOS, macOS, Windows)
3. Whether this is a common enough functionality that a package/components likely exists

### Step 2: Search for cangjie packages/components

while cangjie sdk is not used for search cangjie packages/components.

Run the find command with a relevant query:

```bash
python3 ./scripts/main.py -s [package_name]
```

For example:

- User asks "can you help me with cangjie json encoding?" → `python3 ./scripts/main.py -s json`
- User asks "I need to create a changelog" → `python3 ./scripts/main.py -s changelog`
- User asks "I need to create a http router" → `python3 ./scripts/main.py -s http_router`

The command will return results like:

```
Page 1 results (1 record(s) total, 1 page(s) total):

# | Name        | Latest version | Organization | Publisher | Downloads | Description
--+-------------+----------------+--------------+-----------+-----------+--------------
0 | http_router | 0.1.1          | opencj       | changeden | 4         | restful路径解析工具
```

### Step 3: Download packages/components

When you find relevant packages/components, ask the users if they want to download the packages/components, so the users can view the source code of packages/components:

1. If the users said no, just bypass this step

2. If the users said yes, you get organization, package_name, package_version, the run this command to download packages/components:

   `python3 ./scripts/main.py -d organization::package_name:package_version`

Example response:

```
Saved to: /Users/hxm/Downloads/http_router-0.1.1.pkg
```

now, you have to ask users if they want to config this package/component in their cangjie project.

### Step 4: confirm the users project path

Ask the users to tell you the project path they want to config, you can ask like this:

`Which project do you want to config, i will recommend ~/workspace/cj_pro`

The users may tell you the project path like '/Users/xxx/workspace/pro_name', so you get cangjie_project_path.

### Step 5: Make sure cangjie sdk is installed

1. Run the env command with a grep

`env | grep CANGJIE_HOME`

2. if this command returns nothing, there is no cangjie sdk environment. So,:
   * ask the users to install cangjie sdk from this url : https://cangjie-lang.cn/download, and ask the users to tell you the install path of cangjie sdk path, like '/Users/xxx/cangjie/', so the CJ_SDK_PATH=/Users/xxx/cangjie/
   * or, after you get confirm of the users, you can also help the users to download and extract cangjie sdk from this url:  https://cangjie-lang.cn/download, and you get the extract path as CJ_SDK_PATH

3. if you get CJ_SDK_PATH, then run this command and source the .zshrc, before you run , you replace SDK_PATH with what you get from the last step
   * If you run on macOS/Linux → `echo "source SDK_PATH/envsetup.sh" >> .zshrc & source .zshrc`
   * If you run  on Windows(CMD)→ `setx PATH=%PATH%;SDK_PATH\envsetup.bat`
   * If you run  on Windows(POWERSHELL)→ `$env:Path += ";SDK_PATH\envsetup.bat"`

4. if this command returns like 'CANGJIE_HOME=...', then the cangjie sdk environment is ready.

### Step 6: Init project and import the cangjie package into project 

Now you get three key message :

* cangjie sdk installed

* the user's cangjie_project_path
* Package's organization::package_name:package_version

you can init project, you must replace cangjie_project_path with the place you get from users in step 4 before you run this command:

```bash
cjpm init --path cangjie_project_path
```

then, config the cjpm.toml file in cangjie_project_path, run this command:

- If the organization is 'default'→ `python3 ./scripts/main.py -e cangjie_project_path/cjpm.toml dependencies.package_name package_version`
- if the organization is not 'default' → `python3 ./scripts/main.py -e cangjie_project_path/cjpm.toml dependencies.organization::package_name package_version`

### Step 7: Build the project

Now you can build the user's project, you can run this command:

`cd cangjie_project_path & cjpm build`

Then, you returns the compile results to the users, and tell the users how to run compile results.

### Step 8: Init project and develop a cangjie package

You can ask the users to confirm if they want to develop a cangjie package and publish to [The Cangjie Central Repository](https://pkg.cangjie-lang.cn/index) , 

If the users confirmed, you can init project, you must replace cangjie_project_path with the place you get from users in step 4 before you run this command, you must notice you have to use --type=dynamic when the users want to develop a cangjie package:

```bash
cjpm init --path cangjie_project_path --type=dynamic
```

then you can help the users to coding in this project, you can give the users many tips like this:

`what kind of package or components do you want, we can develop together with Cangjie language.`

Then, you can clone this repo and learn Cangjie language with a grep tool: https://gitcode.com/Cangjie/cangjie_docs/blob/main/docs/dev-guide/summary_cjnative_EN.md

anyway, you can build the new project like Step 7

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                                  |
| --------------- | ------------------------------------------------ |
| static language | Cangjie, Cangjie SDK                             |
| stdx            | Cangjie_stdx, stdx, stdx_xxx, stdx_yyy, stdx_zzz |
| json            | serialization, json_encode                       |
| Documentation   | docs, readme, changelog, api-docs                |
| Code Quality    | review, lint, refactor, best-practices           |
| Design          | ui, ux, design-system, accessibility             |
| Productivity    | workflow, automation, git                        |

## Tips for Effective Searches

1. **Use specific keywords**: "json encoding" is better than just "encoding"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
