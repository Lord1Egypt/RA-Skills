-- 查询用户置顶/刷新消费记录
-- inFlag: 0=消费, 1=充值
-- status: 4和6才是成功状态
-- payTime: 日期格式，无需FROM_UNIXTIME转换
-- subTime: 毫秒时间戳，需要转换
-- 参数: userId

SELECT 
    a.id,
    a.transDetail,
    a.amount,
    a.inFlag,
    a.status,
    a.payTime,
    FROM_UNIXTIME(a.subTime/1000) as subTime
FROM t_accout_trans a 
WHERE a.userId = (SELECT id FROM t_user WHERE userId = ?)
AND a.inFlag = 0
AND a.status IN (4, 6)
AND (a.transDetail LIKE '%置顶%' OR a.transDetail LIKE '%刷新%' OR a.transDetail LIKE '%推荐%')
ORDER BY a.subTime DESC
LIMIT 100;

-- 查询用户总消费金额（成功的消费记录）
-- 参数: userId

SELECT 
    SUM(a.amount) as total_spending,
    COUNT(*) as transaction_count
FROM t_accout_trans a 
WHERE a.userId = (SELECT id FROM t_user WHERE userId = ?)
AND a.inFlag = 0
AND a.status IN (4, 6);

-- 查询用户充值记录（成功的充值）
-- payTime: 日期格式，无需转换
-- 参数: userId

SELECT 
    a.id,
    a.transDetail,
    a.amount,
    a.payTime
FROM t_accout_trans a 
WHERE a.userId = (SELECT id FROM t_user WHERE userId = ?)
AND a.inFlag = 1
AND a.status IN (4, 6)
ORDER BY a.subTime DESC
LIMIT 100;

-- 查询发单人账单（用于分析任务发布者的消费情况）
-- payTime: 日期格式，无需转换
-- subTime: 毫秒时间戳
-- transType: 交易类型代码
-- accoutType: 账户类型 (1000=任务余额, 1001=保证金, 1002=收入分红, 1003=推广收入)
-- 参数: taskNo, claimTime(毫秒时间戳)

SELECT 
    a.id,
    a.transDetail,
    a.amount,
    a.inFlag,
    a.status,
    a.transType,
    a.accoutType,
    a.payTime
FROM t_accout_trans a 
INNER JOIN t_task t ON a.userId = t.userId
WHERE t.taskNo = ? 
AND a.inFlag = 0
AND a.status IN (4, 6)
AND a.subTime < ? 
ORDER BY a.subTime DESC 
LIMIT 10;

-- 查询交易类型名称
-- 参数: transType

SELECT 
    typeCode as transType,
    typeName,
    accoutType,
    `inout` as inFlag,
    remark as remarker
FROM t_accout_transtype 
WHERE typeCode = ?
LIMIT 1;

-- 账户类型说明:
-- 1000 = 任务余额 (置顶/推荐/刷新只能使用此账户)
-- 1001 = 保证金
-- 1002 = 收入分红 (接单收入)
-- 1003 = 推广收入 (平台奖励)

-- 通过手机号查询用户
-- 参数: mobile

SELECT 
    id,
    userId,
    truename,
    mobile,
    FROM_UNIXTIME(regTime/1000) as regTime
FROM t_user 
WHERE mobile = ?
LIMIT 1;

-- ============================================
-- 用户状态查询（注意：userId是数字ID，不是字符串userId）
-- ============================================

-- 查询是否禁言
-- 参数: userId (数字ID)
-- status >= 1 表示被禁言

SELECT status 
FROM t_msg_black 
WHERE userId = ? 
AND status >= 1 
LIMIT 1;

-- 查询是否禁止发单
-- 参数: userId (数字ID)
-- typeId=1 表示发单限制

SELECT reason 
FROM t_task_black 
WHERE id = ? 
AND typeId = 1 
AND status = 1 
LIMIT 1;

-- 查询是否禁止接单
-- 参数: userId (数字ID)
-- typeId=2 表示接单限制

SELECT reason 
FROM t_task_black 
WHERE id = ? 
AND typeId = 2 
AND status = 1 
LIMIT 1;

-- 查询是否禁止充值
-- 参数: userId (数字ID)

SELECT typeId, remarker 
FROM t_hb_black 
WHERE userId = ? 
AND status = 1 
LIMIT 1;

-- 查询账户是否冻结 (方式1: t_accout表)
-- 参数: userId (数字ID)
-- status=100 表示冻结

SELECT attr5 
FROM t_accout 
WHERE userId = ? 
AND status = 100 
LIMIT 1;

-- 查询账户是否冻结 (方式2: t_user_frozen表)
-- 参数: userId (数字ID)
-- status=0 表示冻结中

SELECT reason 
FROM t_user_frozen 
WHERE userId = ? 
AND status = 0 
LIMIT 1;

-- 查询用户账户余额
-- 参数: userId (数字ID)

SELECT d.typeCode as accoutType, d.balance as amount 
FROM t_accout_detail d 
INNER JOIN t_accout a ON d.accoutId = a.id
WHERE a.userId = ?
LIMIT 10;
