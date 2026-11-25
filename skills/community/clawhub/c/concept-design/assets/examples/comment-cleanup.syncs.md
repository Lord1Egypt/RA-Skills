# app Discussion
include Posting
include Commenting [Posting.PostId]

### Remove existing comments on the deleted post
sync RemovePostComments
when { Posting/delete: [] => [post: ?post] }
where { Commenting: { ?comment target: ?post } }
then { Commenting/remove: [comment: ?comment] }

## Execution constraints
- Flow/correlation: emitted remove calls retain the successful Posting/delete occurrence's flow.
- Reads/order: comments are read at rule evaluation after Posting/delete completes.
- Outcomes: each matched row emits one remove call; zero rows emit none. A comment deleted before remove produces the declared false result.
- Timing/recovery: concurrent additions, other removal failures, timing, retry, and restart recovery remain open.
