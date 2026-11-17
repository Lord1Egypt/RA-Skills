# 版本与更新

读取 `VERSION.md` 获取本地版本。每天最多一次请求：

`GET https://blackstone.wansu.tech/api/public/skills/short-fiction/manifest`

远端版本不高于本地版本时继续当前任务。发现新版本时只提示作者，不下载、不替换。只有作者在当前对话明确同意后，才下载到临时目录，按清单核对文件数与每个文件的 SHA-256，校验成功后替换 `blackstone-short-fiction` 目录。

更新只操作短故事版 Skill 自身，不改正文、客户端配置、其他 Skill 或中长篇版。失败时保留原版本并继续当前任务。
