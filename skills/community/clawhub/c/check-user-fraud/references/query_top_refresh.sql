-- 查询任务是否有置顶刷新
-- 参数: submitId (sb.id)

SELECT COUNT(r.id) as top_count 
FROM t_task_submit sb 
INNER JOIN t_task_order r ON sb.taskId = r.taskId
WHERE sb.id = ? 
AND r.startTime > sb.claimTime 
AND r.expiredTime > sb.claimTime 
AND r.status IN (1, 100);