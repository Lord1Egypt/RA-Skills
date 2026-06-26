# KB 读取操作手册

从这个技能执行命令时，把下面的 `kb ...` 命令字符串整体传给 `./scripts/kb_execute.py`，例如：`./scripts/kb_execute.py "kb cat --code DOC_12345"`。
  
当你需要定位仓库、查看目录、搜索内容、读取文档或返回文档链接时，读这个文件。  
  
## 工作流  
  
1. 不知道仓库或目录时，先用 `kb ls`。  
2. 需要看目录层级时，用 `kb tree`，不要拿它代替内容搜索。  
3. 知道主题但不知道具体文件时，用 `kb search`。  
4. 锁定到具体文档后，用 `kb cat` 读取。  
5. 只有在最终答复需要可点击链接时，才用 `kb render`。  
 
## 共享规则  
  
- 一旦拿到仓库或文档 `code`，优先使用 `code`。  
- 路径命中不唯一时，先消歧，再进入修改流程。  
- `kb cat` 返回内容就是后续理解和修改的依据，包括其中的 HTML 结构。  
  
## 命令卡片  
  
### `kb ls`  
  
用于列出可访问仓库，或者列出某个路径下的子项。  
  
- 常用写法：  
  - `kb ls`  
  - `kb ls <repo_or_path>`  
- 常用参数：  
  - `--sort name|updated|size`  
  - `--limit N`  
- 示例：  
  
```text  
kb ls team-workspace/docs --sort updated --limit 50  
```  
  
### `kb tree`  
  
用于在读取前快速理解目录结构。  
  
- 常用写法：  
  - `kb tree <repo/path/> [--depth N] [--limit N]`  
- 适合看层级，不适合替代全文搜索。  
- 示例：  
  
```text  
kb tree team-workspace/docs/project-a/ --depth 2  
```  
  
### `kb search`  
  
用于按主题搜索内容，尤其适合“知道要找什么，但不知道文件名”的场景。  
  
- 常用写法：  
  - `kb search --query "<text>" --repo-code <repo_code>`  
- 常用过滤：  
  - `--path <prefix>`  
  - `--file <glob>`  
  - `--doc-code <code>` 或 `--codes <a,b,c>`  
  - `--mode lex|sem|hybrid`  
  - `--topk N`  
- 示例：  
  
```text  
kb search --query "发布流程" --repo-code TEAM_DOCS --path process/ --mode hybrid --topk 10  
```  
  
### `kb cat`  
  
用于读取你准备摘要、引用或修改的具体文档。  
  
- 常用写法：  
  - `kb cat --code <doc_code>`  
  - `kb cat --name <repo/path.md>`  
- 常用参数：  
  - `--range A:B`  
  - `--head N`  
  - `--tail N`  
  - `-n`  
- 使用要求：  
  - 修改前必须先读。  
  - 后续 patch 内容要基于返回的 HTML。  
- 示例：  
  
```text  
kb cat --code DOC_12345 -n  
```  
  
### `kb render`  
  
用于在最后把文档 `code` 转成可点击链接。  
  
- 常用写法：  
  - `kb render <doc_code,doc_code,...>`  
- 只渲染最终答复里确实需要引用的文档。  
- 示例：  
  
```text  
kb render DOC_12345,DOC_67890  
```  
  
## 不在本文件覆盖的内容

- 新建文档
- 新建目录、移动、删除、发布
- 基于 patch 的精确修改

需要写入或修改时，直接按需阅读本 skill 自带的参考资料：

- 新建与结构操作看 [write.md](./write.md)
- 基于 patch 的精确修改看 [update.md](./update.md)
