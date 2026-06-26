-- AI测试平台数据库初始化脚本
-- 创建时间: 2026-04-16

-- 使用数据库
USE ai_test_platform;

-- 授权码表
CREATE TABLE IF NOT EXISTS auth_codes (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    code VARCHAR(100) UNIQUE NOT NULL COMMENT '授权码(加密后)',
    permission VARCHAR(20) NOT NULL COMMENT '权限类型: all/generate/execute',
    expire_time DATETIME NOT NULL COMMENT '过期时间',
    use_count INT DEFAULT 0 COMMENT '已使用次数',
    max_count INT NOT NULL COMMENT '最大使用次数',
    is_active TINYINT DEFAULT 1 COMMENT '启用状态: 1启用/0禁用',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_code (code),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='授权码表';

-- 测试用例表
CREATE TABLE IF NOT EXISTS test_cases (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    title VARCHAR(200) NOT NULL COMMENT '用例标题',
    content TEXT COMMENT '用例内容',
    type VARCHAR(20) COMMENT '用例类型: api/ui',
    created_by VARCHAR(50) COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测试用例表';

-- 自动化脚本表
CREATE TABLE IF NOT EXISTS auto_scripts (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(200) NOT NULL COMMENT '脚本名称',
    content TEXT COMMENT '脚本内容',
    type VARCHAR(20) COMMENT '脚本类型: api/ui',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态: active/inactive',
    created_by VARCHAR(50) COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='自动化脚本表';

-- 执行记录表
CREATE TABLE IF NOT EXISTS execute_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    script_id INT COMMENT '脚本ID',
    auth_code VARCHAR(100) COMMENT '使用的授权码',
    result VARCHAR(20) COMMENT '执行结果: success/fail',
    log TEXT COMMENT '执行日志',
    execute_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '执行时间',
    duration INT COMMENT '执行时长(秒)',
    INDEX idx_script (script_id),
    INDEX idx_result (result)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='执行记录表';

-- 测试报告表
CREATE TABLE IF NOT EXISTS test_reports (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    record_id INT COMMENT '执行记录ID',
    report_content TEXT COMMENT '报告内容',
    file_path VARCHAR(500) COMMENT '报告文件路径',
    ai_analysis TEXT COMMENT 'AI分析结果',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_record (record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测试报告表';

-- 任务进度表
CREATE TABLE IF NOT EXISTS task_progress (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    task_id VARCHAR(100) UNIQUE NOT NULL COMMENT '任务ID',
    task_type VARCHAR(50) COMMENT '任务类型: generate/execute',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending/processing/completed/failed',
    progress INT DEFAULT 0 COMMENT '进度百分比',
    message TEXT COMMENT '进度消息',
    result_data TEXT COMMENT '结果数据',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_task_id (task_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务进度表';

-- 系统配置表
CREATE TABLE IF NOT EXISTS system_config (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    config_key VARCHAR(100) UNIQUE NOT NULL COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    description VARCHAR(500) COMMENT '配置说明',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 插入默认系统配置
INSERT INTO system_config (config_key, config_value, description) VALUES
('deepseek_api_key', '', 'DeepSeek API密钥'),
('deepseek_base_url', 'https://api.deepseek.com', 'DeepSeek API地址'),
('test_environment_url', 'http://localhost:8080', '测试环境地址'),
('system_initialized', 'false', '系统初始化状态')
ON DUPLICATE KEY UPDATE config_value=VALUES(config_value);

-- 创建授权验证存储过程（安全加固）
DELIMITER $$

CREATE PROCEDURE verify_and_use_auth_code(
    IN p_auth_code VARCHAR(100),
    IN p_required_permission VARCHAR(20),
    OUT p_is_valid BOOLEAN,
    OUT p_message VARCHAR(255),
    OUT p_remaining_count INT
)
BEGIN
    DECLARE v_permission VARCHAR(20);
    DECLARE v_expire_time DATETIME;
    DECLARE v_use_count INT;
    DECLARE v_max_count INT;
    DECLARE v_is_active TINYINT;

    -- 查询授权码信息
    SELECT
        permission,
        expire_time,
        use_count,
        max_count,
        is_active
    INTO
        v_permission,
        v_expire_time,
        v_use_count,
        v_max_count,
        v_is_active
    FROM auth_codes
    WHERE code = p_auth_code;

    -- 验证授权码
    IF v_is_active IS NULL THEN
        SET p_is_valid = FALSE;
        SET p_message = '授权码不存在';
        SET p_remaining_count = 0;
    ELSEIF v_is_active = 0 THEN
        SET p_is_valid = FALSE;
        SET p_message = '授权码已被禁用';
        SET p_remaining_count = 0;
    ELSEIF v_expire_time < NOW() THEN
        SET p_is_valid = FALSE;
        SET p_message = '授权码已过期';
        SET p_remaining_count = 0;
    ELSEIF v_use_count >= v_max_count THEN
        SET p_is_valid = FALSE;
        SET p_message = '授权码使用次数已达上限';
        SET p_remaining_count = 0;
    ELSEIF p_required_permission = 'generate' AND v_permission = 'execute' THEN
        SET p_is_valid = FALSE;
        SET p_message = '权限不足：需要生成权限';
        SET p_remaining_count = v_max_count - v_use_count;
    ELSEIF p_required_permission = 'execute' AND v_permission = 'generate' THEN
        SET p_is_valid = FALSE;
        SET p_message = '权限不足：需要执行权限';
        SET p_remaining_count = v_max_count - v_use_count;
    ELSE
        -- 验证通过，增加使用次数
        UPDATE auth_codes
        SET use_count = use_count + 1
        WHERE code = p_auth_code;

        SET p_is_valid = TRUE;
        SET p_message = '授权验证成功';
        SET p_remaining_count = v_max_count - v_use_count - 1;
    END IF;
END$$

DELIMITER ;

-- 数据库初始化完成
SELECT '数据库初始化完成！' AS message;
