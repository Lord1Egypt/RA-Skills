# app Discussion
include Posting
include Commenting [Posting.PostId]

### 删除目标文章的现存评论
sync RemovePostComments
when { Posting/delete: [] => [post: ?post] }
where { Commenting: { ?comment target: ?post } }
then { Commenting/remove: [comment: ?comment] }

## 执行约束
- flow/关联：发出的 remove 调用沿用 Posting/delete 成功发生记录的 flow。
- 读取/顺序：Posting/delete 完成后，规则才读取求值时的评论。
- 结果：每条匹配行发出一次 remove，零行不调用；评论在 remove 前被删除时，返回声明的 false 结果。
- 时限/恢复：并发新增、其他删除失败、时限、重试与重启恢复仍未决。
