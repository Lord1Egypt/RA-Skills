-- 查询用户做单情况
-- 参数: userId

SELECT 
    sb.id, 
    sb.taskAmout,
    sb.examineText,
    t.taskNo,
    t.title,
    s.deviceId,
    sb.`status`,
    FROM_UNIXTIME(sb.claimTime/1000) as '报名时间',
    FROM_UNIXTIME(sb.subTime/1000) as '提交时间',
    FROM_UNIXTIME(sb.examineTime/1000) as '审核时间',
    u.userId,
    c.provice,
    c.city,
    s.appId,
    s.channel,
    t.userNo,
    sb.ip 
FROM t_task_subctx s 
INNER JOIN t_task_submit sb ON sb.id = s.subId
INNER JOIN t_task t ON sb.taskId = t.id
INNER JOIN t_user u ON u.id = sb.subId
INNER JOIN t_ip_config c ON c.id = INET_ATON(s.ip)
WHERE u.userId = ? AND sb.`status` = 2 
ORDER BY sb.claimTime DESC 
LIMIT 100;