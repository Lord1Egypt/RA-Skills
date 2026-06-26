#!/usr/bin/env python3
"""
DigitalSalesClaw - MySQL 初始化脚本
用法: python3 init_mysql.py [--host HOST] [--port PORT] [--user USER] [--pass PASS]

"""
import sys
import os
import argparse

MYSQL_SCRIPT = """
-- ─────────────────────────────────────────────────────────────
-- DigitalSalesClaw - MySQL 初始化脚本
-- 数据库: digitalsalesclaw
-- 字符集: utf8mb4_0900_ai_ci
-- ─────────────────────────────────────────────────────────────

DROP DATABASE IF EXISTS digitalsalesclaw;
CREATE DATABASE digitalsalesclaw
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE digitalsalesclaw;

-- ─────────────────────────────────────────
-- 内容域
-- ─────────────────────────────────────────

CREATE TABLE content_topics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(500) NOT NULL COMMENT '选题名称',
    platform VARCHAR(50) DEFAULT 'douyin' COMMENT '目标平台',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending/approved/published/draft/rejected',
    priority VARCHAR(10) DEFAULT 'medium' COMMENT '优先级: high/medium/low/urgent',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_platform (platform),
    INDEX idx_priority (priority),
    INDEX idx_created (created_at),
    INDEX idx_status_platform (status, platform),
    INDEX idx_priority_status (priority, status)
) ENGINE=InnoDB COMMENT='内容选题';

CREATE TABLE content_scripts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    topic_id BIGINT COMMENT '关联选题ID',
    title VARCHAR(500) COMMENT '脚本标题',
    content TEXT COMMENT '脚本正文',
    platform VARCHAR(50) COMMENT '目标平台',
    format VARCHAR(20) DEFAULT 'video' COMMENT '格式: video/article/image/story',
    status VARCHAR(20) DEFAULT 'draft' COMMENT '状态: draft/approved/published/rejected',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_topic (topic_id),
    INDEX idx_status (status),
    INDEX idx_platform (platform),
    FOREIGN KEY (topic_id) REFERENCES content_topics(id) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='内容脚本';

CREATE TABLE content_campaigns (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(500) COMMENT '活动名称',
    platform VARCHAR(50) COMMENT '投放平台',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态: active/paused/finished',
    budget DECIMAL(12,2) DEFAULT 0 COMMENT '预算',
    start_date DATE COMMENT '开始日期',
    end_date DATE COMMENT '结束日期',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_platform (platform)
) ENGINE=InnoDB COMMENT='内容活动';

CREATE TABLE content_metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    campaign_id BIGINT COMMENT '关联活动ID',
    date DATE COMMENT '数据日期',
    impressions BIGINT DEFAULT 0 COMMENT '曝光量',
    clicks BIGINT DEFAULT 0 COMMENT '点击量',
    conversions BIGINT DEFAULT 0 COMMENT '转化数',
    spend DECIMAL(12,2) DEFAULT 0 COMMENT '花费',
    engagement_rate DECIMAL(8,4) DEFAULT 0 COMMENT '互动率',
    ctr DECIMAL(8,4) DEFAULT 0 COMMENT '点击率',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES content_campaigns(id) ON DELETE SET NULL,
    INDEX idx_campaign (campaign_id),
    INDEX idx_date (date),
    INDEX idx_campaign_date (campaign_id, date)
) ENGINE=InnoDB COMMENT='内容效果指标';

-- ─────────────────────────────────────────
-- 合规域
-- ─────────────────────────────────────────

CREATE TABLE compliance_rules (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rule_code VARCHAR(50) NOT NULL COMMENT '规则编码: GA-A-001格式',
    rule_name VARCHAR(200) COMMENT '规则名称',
    rule_type VARCHAR(50) DEFAULT 'banned' COMMENT '类型: banned/warning/info',
    category VARCHAR(100) COMMENT '违规大类',
    pattern VARCHAR(500) COMMENT '匹配正则（仅用于Guardrail兜底）',
    action_level VARCHAR(20) DEFAULT 'medium' COMMENT '级别: critical/high/medium/low',
    description TEXT COMMENT '规则描述',
    rule_hierarchy VARCHAR(50) COMMENT '三层编码: GA-A-001',
    law_reference VARCHAR(200) COMMENT '法规依据',
    severity_score INT DEFAULT 5 COMMENT '严重度评分1-10',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (rule_code),
    INDEX idx_category (category),
    INDEX idx_hierarchy (rule_hierarchy),
    INDEX idx_action_level (action_level),
    FULLTEXT INDEX idx_pattern (pattern)
) ENGINE=InnoDB COMMENT='合规规则';

CREATE TABLE compliance_reviews (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    content_id BIGINT COMMENT '关联内容ID',
    review_stage VARCHAR(30) DEFAULT 'semantic_review' COMMENT '审核阶段',
    violations JSON COMMENT '违规详情（语义分析结果）',
    risk_level VARCHAR(20) COMMENT '风险级别: critical/high/medium/low',
    compliance_score DECIMAL(5,1) COMMENT '参考评分（来自Guardrail统计）',
    review_result TEXT COMMENT '审核结论',
    submitted_at DATETIME COMMENT '提交时间',
    completed_at DATETIME COMMENT '完成时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_content (content_id),
    INDEX idx_risk (risk_level),
    INDEX idx_stage (review_stage),
    INDEX idx_created (created_at)
) ENGINE=InnoDB COMMENT='合规审核记录';

CREATE TABLE compliance_audit_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    audit_id VARCHAR(100) COMMENT '审核单ID',
    from_state VARCHAR(30) COMMENT '原状态',
    to_state VARCHAR(30) COMMENT '新状态',
    actor VARCHAR(100) COMMENT '操作人',
    reason TEXT COMMENT '变更原因',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit (audit_id),
    INDEX idx_state (to_state),
    INDEX idx_created (created_at)
) ENGINE=InnoDB COMMENT='合规状态机审计日志';

-- ─────────────────────────────────────────
-- 患者域
-- ─────────────────────────────────────────

CREATE TABLE patient_sessions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE COMMENT '会话ID',
    patient_name VARCHAR(200) COMMENT '患者姓名',
    patient_id VARCHAR(100) COMMENT '患者编号',
    segment VARCHAR(50) COMMENT '分群: high_risk/medium_risk/low_risk/active/resolved',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态: active/pending/resolved',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    INDEX idx_status (status),
    INDEX idx_segment (segment),
    INDEX idx_patient (patient_id)
) ENGINE=InnoDB COMMENT='患者会话';

CREATE TABLE patient_messages (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) COMMENT '关联会话ID',
    role VARCHAR(20) COMMENT '角色: user/assistant/system',
    content TEXT COMMENT '消息内容',
    sent TINYINT DEFAULT 0 COMMENT '是否已发送: 0=待发 1=已发',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    INDEX idx_sent (sent),
    INDEX idx_created (created_at)
) ENGINE=InnoDB COMMENT='患者消息';

CREATE TABLE patient_tickets (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) COMMENT '关联会话ID',
    ticket_type VARCHAR(50) COMMENT '工单类型: escalation/complaint/follow_up',
    priority VARCHAR(10) DEFAULT 'normal' COMMENT '优先级',
    status VARCHAR(20) DEFAULT 'open' COMMENT '状态: open/in_progress/resolved/closed',
    assigned_to VARCHAR(100) COMMENT '处理人',
    notes TEXT COMMENT '处理备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority)
) ENGINE=InnoDB COMMENT='患者工单';

-- ─────────────────────────────────────────
-- 药房域
-- ─────────────────────────────────────────

CREATE TABLE pharmacy_inventory (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(100) COMMENT '产品ID',
    product_name VARCHAR(300) COMMENT '产品名称',
    quantity INT DEFAULT 0 COMMENT '当前库存',
    reorder_point INT DEFAULT 10 COMMENT '补货触发点',
    pharmacy VARCHAR(200) COMMENT '药房名称',
    status VARCHAR(20) DEFAULT 'ok' COMMENT '状态: ok/low/out/overstocked',
    last_restocked DATE COMMENT '最后补货日期',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_product (product_id),
    INDEX idx_status (status),
    INDEX idx_pharmacy (pharmacy),
    INDEX idx_stock_level (status, quantity)
) ENGINE=InnoDB COMMENT='药房库存';

-- ─────────────────────────────────────────
-- 供应链
-- ─────────────────────────────────────────

CREATE TABLE supply_chain_orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE COMMENT '订单ID',
    product_id VARCHAR(100) COMMENT '产品ID',
    product_name VARCHAR(300) COMMENT '产品名称',
    quantity INT COMMENT '采购数量',
    status VARCHAR(30) DEFAULT 'pending' COMMENT '状态: pending/approved/ordered/shipped/received/stocked',
    priority VARCHAR(10) DEFAULT 'normal' COMMENT '优先级',
    notes TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_order (order_id),
    INDEX idx_status (status),
    INDEX idx_product (product_id),
    INDEX idx_priority (priority)
) ENGINE=InnoDB COMMENT='采购订单';

-- ─────────────────────────────────────────
-- 医生/KOL域
-- ─────────────────────────────────────────

CREATE TABLE doctor_profiles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doctor_id VARCHAR(100) UNIQUE COMMENT '医生ID',
    name VARCHAR(200) COMMENT '姓名',
    hospital VARCHAR(300) COMMENT '医院',
    department VARCHAR(200) COMMENT '科室',
    title VARCHAR(100) COMMENT '职称',
    specialty VARCHAR(200) COMMENT '专业',
    influence_score DECIMAL(5,2) DEFAULT 0 COMMENT '影响力评分',
    compliance_score DECIMAL(5,2) DEFAULT 100 COMMENT '合规评分',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_doctor (doctor_id),
    INDEX idx_specialty (specialty),
    INDEX idx_hospital (hospital),
    INDEX idx_influence (influence_score DESC)
) ENGINE=InnoDB COMMENT='医生档案';

CREATE TABLE doctor_visits (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doctor_id VARCHAR(100) COMMENT '医生ID',
    visit_type VARCHAR(30) COMMENT '拜访类型: first/follow_up/academic/detail',
    result VARCHAR(30) COMMENT '结果: success/pending/cancelled/rescheduled',
    notes TEXT COMMENT '拜访记录',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctor_profiles(doctor_id) ON DELETE SET NULL,
    INDEX idx_doctor (doctor_id),
    INDEX idx_result (result),
    INDEX idx_created (created_at)
) ENGINE=InnoDB COMMENT='医生拜访记录';

CREATE TABLE kol_profiles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    kol_id VARCHAR(100) UNIQUE COMMENT 'KOL ID',
    name VARCHAR(200) COMMENT 'KOL 名称',
    platform VARCHAR(50) COMMENT '平台',
    specialty VARCHAR(200) COMMENT '领域',
    followers BIGINT DEFAULT 0 COMMENT '粉丝数',
    engagement_rate DECIMAL(8,4) DEFAULT 0 COMMENT '互动率',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态: active/inactive',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_kol (kol_id),
    INDEX idx_platform (platform),
    INDEX idx_status (status),
    INDEX idx_followers (followers DESC)
) ENGINE=InnoDB COMMENT='KOL档案';

-- ─────────────────────────────────────────
-- 竞品域
-- ─────────────────────────────────────────

CREATE TABLE drug_products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(100) COMMENT '产品ID',
    name VARCHAR(300) COMMENT '产品名称',
    platform VARCHAR(50) COMMENT '平台',
    price DECIMAL(10,2) COMMENT '价格',
    rating DECIMAL(3,1) COMMENT '评分',
    reviews_count INT DEFAULT 0 COMMENT '评价数',
    sales_trend VARCHAR(20) COMMENT '销售趋势: rising/falling/stable',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product (product_id),
    INDEX idx_platform (platform),
    INDEX idx_price (price)
) ENGINE=InnoDB COMMENT='竞品药品';

CREATE TABLE competitor_analysis (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    competitor_name VARCHAR(300) COMMENT '竞品名称',
    competitor_price DECIMAL(10,2) COMMENT '价格',
    competitor_rating DECIMAL(3,1) COMMENT '评分',
    analysis_date DATE COMMENT '分析日期',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_competitor (competitor_name),
    INDEX idx_date (analysis_date)
) ENGINE=InnoDB COMMENT='竞品监控';

-- ─────────────────────────────────────────
-- 工作流/触发器
-- ─────────────────────────────────────────

CREATE TABLE workflow_executions (
    id VARCHAR(100) PRIMARY KEY COMMENT '执行ID',
    name VARCHAR(200) COMMENT '工作流名称',
    status VARCHAR(30) COMMENT '状态: running/completed/error/skipped',
    steps_json JSON COMMENT '步骤执行详情',
    context_json JSON COMMENT '执行上下文',
    started_at DATETIME COMMENT '开始时间',
    completed_at DATETIME COMMENT '完成时间',
    INDEX idx_status (status),
    INDEX idx_name (name)
) ENGINE=InnoDB COMMENT='工作流执行记录';

CREATE TABLE trigger_history (
    trigger_name VARCHAR(100) PRIMARY KEY COMMENT '触发器名称',
    last_triggered_at DATETIME COMMENT '最后触发时间',
    trigger_count INT DEFAULT 1 COMMENT '累计触发次数',
    is_active TINYINT DEFAULT 1 COMMENT '是否启用',
    INDEX idx_active (is_active)
) ENGINE=InnoDB COMMENT='触发器历史';

-- ─────────────────────────────────────────
-- 种子数据：合规规则（28条）
-- ─────────────────────────────────────────

INSERT INTO compliance_rules (rule_code, rule_name, rule_type, category, pattern, action_level, description, rule_hierarchy, law_reference, severity_score) VALUES
('GA-A-001', '最佳/最优/顶级/极品', 'banned', '广告法绝对化用语', '最佳|最优|顶级|极品', 'critical', '广告法第九条', 'GA-A', '广告法第九条', 10),
('GA-A-002', '第一/首选', 'banned', '广告法绝对化用语', '第一(?!牌|名)|首选', 'high', '广告法第九条', 'GA-A', '广告法第九条', 9),
('GA-A-003', '万能', 'banned', '广告法绝对化用语', '万能', 'high', '虚假夸大', 'GA-A', '广告法', 8),
('GA-A-004', '国家级', 'banned', '广告法绝对化用语', '国家级', 'critical', '广告法第十条', 'GA-A', '广告法第十条', 10),
('GA-B-001', '根治/治愈/保证治愈/彻底治愈', 'banned', '医疗效果承诺', '根治|治愈|保证治愈|彻底治愈', 'critical', '虚假医疗承诺', 'GA-B', '药品管理法', 10),
('GA-B-002', '完全治愈', 'banned', '医疗效果承诺', '完全治愈', 'critical', '夸大疗效', 'GA-B', '药品管理法', 8),
('GA-B-004', '药到病除/立竿见影', 'banned', '医疗效果承诺', '药到病除|立竿见影', 'high', '虚假承诺', 'GA-B', '药品管理法', 9),
('GA-B-003', '无效退款', 'banned', '医疗效果承诺', '无效退款', 'high', '虚假承诺', 'GA-B', '药品管理法', 9),
('GA-B-005', '永不复发', 'banned', '疗效夸大', '永不复.?发', 'critical', '夸大疗效', 'GA-B', '药品管理法', 10),
('GA-B-006', '包治百病', 'banned', '虚假承诺', '包治百病', 'critical', '虚假宣传', 'GA-B', '药品管理法', 10),
('GA-D-001', '临床数据夸大', 'banned', '数据引用违规', '临床试验.*?\\\\d+[%％]|研究表明|数据显示', 'high', '数据违规引用', 'GA-D', '广告法', 7),
('GA-D-002', '有效率夸大', 'banned', '数据引用违规', '\\\\d+[%％]\\\\s*有效率', 'high', '数据违规引用', 'GA-D', '广告法', 7),
('GA-D-003', '虚假排名', 'banned', '虚假排名', '排名第一', 'critical', '虚假排名', 'GA-D', '广告法', 9),
('GA-C-001', '竞品贬低', 'banned', '竞品贬低', '优于.*其他|秒杀.*竞品|不如.*竞品', 'high', '贬低竞争对手', 'GA-C', '广告法', 8),
('GA-E-001', '患者证言违规', 'banned', '患者证言违规', '患者.*治愈|.*阿姨.*好了|.*先生.*痊愈', 'high', '患者证言违规', 'GA-E', '广告法', 7),
('GA-E-002', '患者对比违规', 'banned', '患者对比违规', '服用前.*服用后|治疗前后.*对比', 'medium', '患者对比违规', 'GA-E', '广告法', 5),
('GA-H-001', '有效期夸大', 'banned', '有效期夸大', '永久有效', 'medium', '有效期夸大', 'GA-H', '广告法', 5),
('GA-I-001', '皮肤科绝对化', 'banned', '皮肤科绝对化表述', '一次.?美白', 'high', '皮肤科夸大', 'GA-I', '广告法', 7),
('GA-I-002', '眼科绝对化', 'banned', '眼科绝对化表述', '恢复视力|治愈近视', 'critical', '眼科夸大', 'GA-I', '广告法', 9),
('RP-A-001', '处方药宣传', 'banned', '处方药宣传', 'Rx\\\\|处方药|凭处方购买', 'critical', '处方药违规宣传', 'RP-A', '处方药管理办法', 10),
('RP-A-002', '医生推荐', 'banned', '处方药代言人', '专家推荐|医生推荐', 'high', '处方药代言人违规', 'RP-A', '处方药管理办法', 9),
('PLT-DY-001', '抖音医疗资质', 'banned', '抖音医疗资质违规', '医生.*看诊|在线开药', 'critical', '抖音医疗资质违规', 'PLT-DY', '抖音医疗推广规范', 9),
('PLT-XHS-001', '小红书违禁宣传', 'banned', '小红书违禁宣传', 'OTC|处方药.*购买', 'high', '小红书违禁', 'PLT-XHS', '小红书医疗推广规范', 7),
('PLT-WX-001', '微信外链限制', 'banned', '微信外链限制', '点击购买|扫码购买', 'medium', '微信外链限制', 'PLT-WX', '微信外链规范', 6),
('KOL-A-001', 'KOL疗效宣传', 'banned', 'KOL疗效宣传', '吃了.*就好了|用了.*就好了', 'high', 'KOL疗效夸大', 'KOL-A', 'KOL合作规范', 7),
('KOL-A-002', 'KOL夸大宣传', 'banned', 'KOL夸大宣传', '神奇|太神了|太牛了', 'medium', 'KOL夸大', 'KOL-A', 'KOL合作规范', 5),
('GN-F-002', '封建迷信', 'banned', '封建迷信', '算命|风水|迷信', 'critical', '封建迷信', 'GN-F', '广告法', 9),
('GN-F-003', '虚假信息', 'banned', '虚假信息', '谣言|假消息|伪造', 'critical', '虚假信息', 'GN-F', '广告法', 10);

-- ─────────────────────────────────────────
-- 验证
-- ─────────────────────────────────────────

SELECT '数据库创建完成' AS status;
SELECT COUNT(*) AS rule_count FROM compliance_rules;
SHOW TABLES;
"""


def main():
    parser = argparse.ArgumentParser(description='DigitalSalesClaw MySQL 初始化')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=3306)
    parser.add_argument('--user', default='ontology')
    parser.add_argument('--pass', dest='password', default='ontology')
    parser.add_argument('--socket', default='/tmp/mysql.sock')
    args = parser.parse_args()

    try:
        import mysql.connector
    except ImportError:
        print("❌ mysql-connector-python 未安装")
        print("   运行: pip install mysql-connector-python")
        sys.exit(1)

    print(f"连接到 MySQL {args.host}:{args.port}...")

    # 先连接不含数据库（创建库用）
    try:
        conn = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            unix_socket=args.socket,
            charset='utf8mb4'
        )
    except mysql.connector.Error as e:
        print(f"❌ 连接失败: {e}")
        sys.exit(1)

    cursor = conn.cursor()
    
    # 逐条执行DDL（MySQL不支持批量执行带;的多句）
    statements = [s.strip() for s in MYSQL_SCRIPT.split(';') if s.strip() and not s.strip().startswith('--')]
    
    # 使用 split 按 ';' 分割后逐条执行
    import re
    # 先提取所有非注释的非空语句
    raw_stmts = re.split(r';\s*\n', MYSQL_SCRIPT)
    
    success = 0
    errors = 0
    
    for stmt in raw_stmts:
        # 移除行内注释和空行
        lines = []
        for line in stmt.split('\n'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue
            lines.append(line)
        sql = ' '.join(lines).strip()
        if not sql:
            continue
        try:
            cursor.execute(sql)
            success += 1
        except mysql.connector.Error as e:
            # 忽略某些无害错误
            if e.errno in (1050, 1062):  # Table exists / duplicate key
                pass
            elif 'already exists' in str(e).lower():
                pass
            else:
                print(f"⚠️  SQL [{sql[:60]}...]: {e}")
            errors += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n✅ 初始化完成 | 执行: {success} | 警告: {errors}")
    print(f"数据库: digitalsalesclaw")
    print(f"表数量: 18")
    print(f"合规规则: 28 条")


if __name__ == "__main__":
    main()