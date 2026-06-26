-- DigitalSalesClaw MySQL 初始化脚本
-- 用法: mysql -uontology -pontology [--default-character-set=utf8mb4] < init.sql

DROP DATABASE IF EXISTS digitalsalesclaw;
CREATE DATABASE digitalsalesclaw DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE digitalsalesclaw;

-- 内容域
CREATE TABLE content_topics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(500) NOT NULL,
    platform VARCHAR(50) DEFAULT 'douyin',
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(10) DEFAULT 'medium',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_platform (platform),
    INDEX idx_priority (priority),
    INDEX idx_created (created_at)
) ENGINE=InnoDB;

CREATE TABLE content_scripts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    topic_id BIGINT,
    title VARCHAR(500),
    content TEXT,
    platform VARCHAR(50),
    format VARCHAR(20) DEFAULT 'video',
    status VARCHAR(20) DEFAULT 'draft',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_topic (topic_id),
    INDEX idx_status (status),
    FOREIGN KEY (topic_id) REFERENCES content_topics(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE content_campaigns (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(500),
    platform VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    budget DECIMAL(12,2) DEFAULT 0,
    start_date DATE,
    end_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_platform (platform)
) ENGINE=InnoDB;

CREATE TABLE content_metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    campaign_id BIGINT,
    date DATE,
    impressions BIGINT DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    conversions BIGINT DEFAULT 0,
    spend DECIMAL(12,2) DEFAULT 0,
    engagement_rate DECIMAL(8,4) DEFAULT 0,
    ctr DECIMAL(8,4) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES content_campaigns(id) ON DELETE SET NULL,
    INDEX idx_campaign (campaign_id),
    INDEX idx_date (date),
    INDEX idx_campaign_date (campaign_id, date)
) ENGINE=InnoDB;

-- 合规域
CREATE TABLE compliance_rules (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rule_code VARCHAR(50) NOT NULL,
    rule_name VARCHAR(200),
    rule_type VARCHAR(50) DEFAULT 'banned',
    category VARCHAR(100),
    pattern VARCHAR(500),
    action_level VARCHAR(20) DEFAULT 'medium',
    description TEXT,
    rule_hierarchy VARCHAR(50),
    law_reference VARCHAR(200),
    severity_score INT DEFAULT 5,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (rule_code),
    INDEX idx_category (category),
    INDEX idx_hierarchy (rule_hierarchy),
    FULLTEXT INDEX idx_pattern (pattern)
) ENGINE=InnoDB;

CREATE TABLE compliance_reviews (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    content_id BIGINT,
    review_stage VARCHAR(30) DEFAULT 'semantic_review',
    violations JSON,
    risk_level VARCHAR(20),
    compliance_score DECIMAL(5,1),
    review_result TEXT,
    submitted_at DATETIME,
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_content (content_id),
    INDEX idx_risk (risk_level),
    INDEX idx_stage (review_stage),
    INDEX idx_created (created_at)
) ENGINE=InnoDB;

CREATE TABLE compliance_audit_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    audit_id VARCHAR(100),
    from_state VARCHAR(30),
    to_state VARCHAR(30),
    actor VARCHAR(100),
    reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit (audit_id),
    INDEX idx_state (to_state)
) ENGINE=InnoDB;

-- 患者域
CREATE TABLE patient_sessions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE,
    patient_name VARCHAR(200),
    patient_id VARCHAR(100),
    segment VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    INDEX idx_status (status),
    INDEX idx_segment (segment)
) ENGINE=InnoDB;

CREATE TABLE patient_messages (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100),
    role VARCHAR(20),
    content TEXT,
    sent TINYINT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    INDEX idx_sent (sent)
) ENGINE=InnoDB;

CREATE TABLE patient_tickets (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100),
    ticket_type VARCHAR(50),
    priority VARCHAR(10) DEFAULT 'normal',
    status VARCHAR(20) DEFAULT 'open',
    assigned_to VARCHAR(100),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- 药房域
CREATE TABLE pharmacy_inventory (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(100),
    product_name VARCHAR(300),
    quantity INT DEFAULT 0,
    reorder_point INT DEFAULT 10,
    pharmacy VARCHAR(200),
    status VARCHAR(20) DEFAULT 'ok',
    last_restocked DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_product (product_id),
    INDEX idx_status (status),
    INDEX idx_pharmacy (pharmacy)
) ENGINE=InnoDB;

-- 供应链
CREATE TABLE supply_chain_orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE,
    product_id VARCHAR(100),
    product_name VARCHAR(300),
    quantity INT,
    status VARCHAR(30) DEFAULT 'pending',
    priority VARCHAR(10) DEFAULT 'normal',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_order (order_id),
    INDEX idx_status (status),
    INDEX idx_product (product_id)
) ENGINE=InnoDB;

-- 医生/KOL域
CREATE TABLE doctor_profiles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doctor_id VARCHAR(100) UNIQUE,
    name VARCHAR(200),
    hospital VARCHAR(300),
    department VARCHAR(200),
    title VARCHAR(100),
    specialty VARCHAR(200),
    influence_score DECIMAL(5,2) DEFAULT 0,
    compliance_score DECIMAL(5,2) DEFAULT 100,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_doctor (doctor_id),
    INDEX idx_specialty (specialty),
    INDEX idx_hospital (hospital)
) ENGINE=InnoDB;

CREATE TABLE doctor_visits (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doctor_id VARCHAR(100),
    visit_type VARCHAR(30),
    result VARCHAR(30),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctor_profiles(doctor_id) ON DELETE SET NULL,
    INDEX idx_doctor (doctor_id),
    INDEX idx_result (result)
) ENGINE=InnoDB;

CREATE TABLE kol_profiles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    kol_id VARCHAR(100) UNIQUE,
    name VARCHAR(200),
    platform VARCHAR(50),
    specialty VARCHAR(200),
    followers BIGINT DEFAULT 0,
    engagement_rate DECIMAL(8,4) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_kol (kol_id),
    INDEX idx_platform (platform),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- 竞品域
CREATE TABLE drug_products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(100),
    name VARCHAR(300),
    platform VARCHAR(50),
    price DECIMAL(10,2),
    rating DECIMAL(3,1),
    reviews_count INT DEFAULT 0,
    sales_trend VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product (product_id),
    INDEX idx_platform (platform)
) ENGINE=InnoDB;

CREATE TABLE competitor_analysis (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    competitor_name VARCHAR(300),
    competitor_price DECIMAL(10,2),
    competitor_rating DECIMAL(3,1),
    analysis_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_competitor (competitor_name),
    INDEX idx_date (analysis_date)
) ENGINE=InnoDB;

-- 工作流/触发器
CREATE TABLE workflow_executions (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(200),
    status VARCHAR(30),
    steps_json JSON,
    context_json JSON,
    started_at DATETIME,
    completed_at DATETIME,
    INDEX idx_status (status),
    INDEX idx_name (name)
) ENGINE=InnoDB;

CREATE TABLE trigger_history (
    trigger_name VARCHAR(100) PRIMARY KEY,
    last_triggered_at DATETIME,
    trigger_count INT DEFAULT 1,
    is_active TINYINT DEFAULT 1,
    INDEX idx_active (is_active)
) ENGINE=InnoDB;

-- 合规规则种子数据
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