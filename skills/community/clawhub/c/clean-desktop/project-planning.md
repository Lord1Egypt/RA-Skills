# 创业大赛报名官网项目

## 项目概述
- 项目名称：创业大赛报名官网
- 技术栈：ThinkPHP 6 + Vue.js + MySQL
- 预算：8000元
- 移动端适配：支持响应式设计

## 功能模块

### 1. 前端（Vue.js）
- **首页**
  - 大赛介绍
  - 报名入口
  - 赛程安排预览
  - 最新公告
  
- **报名表单**
  - 团队信息填写
  - 项目详细介绍
  - 团队成员信息
  - 联系方式
  - 提交状态显示
  
- **个人中心**
  - 报名状态查询
  - 报名信息查看/修改
  - 通知消息查看
  
- **赛事展示**
  - 赛程安排
  - 评委介绍
  - 比赛规则

### 2. 后端（ThinkPHP 6）
- **用户管理**
  - 注册/登录
  - 个人信息管理
  - 权限控制（选手/评委/管理员）
  
- **报名管理**
  - 报名信息CRUD
  - 报名状态管理
  - 报名统计
  
- **赛事管理**
  - 赛程管理
  - 评委管理
  - 评分系统
  
- **通知系统**
  - 公告发布
  - 消息推送
  - 邮件通知

### 3. 数据库设计

#### 3.1 用户表 (users)
```sql
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `email` varchar(100) NOT NULL COMMENT '邮箱',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `role` enum('admin', 'judge', 'participant') NOT NULL DEFAULT 'participant' COMMENT '角色',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

#### 3.2 报名表 (registrations)
```sql
CREATE TABLE `registrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `team_name` varchar(100) NOT NULL COMMENT '团队名称',
  `project_name` varchar(100) NOT NULL COMMENT '项目名称',
  `project_desc` text NOT NULL COMMENT '项目简介',
  `project_detail` text COMMENT '项目详细介绍',
  `category` varchar(50) DEFAULT NULL COMMENT '参赛类别',
  `stage` enum('preliminary', 'semi_final', 'final') DEFAULT 'preliminary' COMMENT '当前阶段',
  `status` enum('pending', 'approved', 'rejected', 'withdrawn') DEFAULT 'pending' COMMENT '状态',
  `score` decimal(10,2) DEFAULT NULL COMMENT '得分',
  `comments` text COMMENT '评委意见',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报名表';
```

#### 3.3 赛程表 (schedules)
```sql
CREATE TABLE `schedules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL COMMENT '标题',
  `stage` enum('preliminary', 'semi_final', 'final') NOT NULL COMMENT '比赛阶段',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `location` varchar(200) DEFAULT NULL COMMENT '地点',
  `description` text COMMENT '描述',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否激活',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='赛程表';
```

#### 3.4 公告表 (announcements)
```sql
CREATE TABLE `announcements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '内容',
  `type` enum('notice', 'important', 'result') DEFAULT 'notice' COMMENT '类型',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否激活',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公告表';
```

#### 3.5 评委表 (judges)
```sql
CREATE TABLE `judges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `expertise` varchar(200) DEFAULT NULL COMMENT '专长领域',
  `title` varchar(100) DEFAULT NULL COMMENT '职称',
  `company` varchar(200) DEFAULT NULL COMMENT '所属公司',
  `bio` text COMMENT '个人简介',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评委表';
```

#### 3.6 评分表 (scores)
```sql
CREATE TABLE `scores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registration_id` int(11) NOT NULL COMMENT '报名ID',
  `judge_id` int(11) NOT NULL COMMENT '评委ID',
  `creativity` decimal(5,2) DEFAULT NULL COMMENT '创新性',
  `feasibility` decimal(5,2) DEFAULT NULL COMMENT '可行性',
  `market_potential` decimal(5,2) DEFAULT NULL COMMENT '市场潜力',
  `team_strength` decimal(5,2) DEFAULT NULL COMMENT '团队能力',
  `presentation` decimal(5,2) DEFAULT NULL COMMENT '表达能力',
  `total_score` decimal(10,2) DEFAULT NULL COMMENT '总分',
  `comments` text COMMENT '评语',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `registration_id` (`registration_id`),
  KEY `judge_id` (`judge_id`),
  FOREIGN KEY (`registration_id`) REFERENCES `registrations` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`judge_id`) REFERENCES `judges` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评分表';
```

## 项目进度计划

### 第一阶段：基础搭建（3天）
- [x] 项目需求分析和设计
- [ ] 创建项目目录结构
- [ ] 数据库设计和建表
- [ ] ThinkPHP 6基础框架搭建
- [ ] Vue.js前端项目初始化

### 第二阶段：核心功能开发（7天）
- [ ] 用户注册登录系统
- [ ] 报名表单开发
- [ ] 报名状态查询
- [ ] 赛程安排展示
- [ ] 通知公告系统

### 第三阶段：评委和管理功能（5天）
- [ ] 评委系统
- [ ] 评分系统
- [ ] 管理后台
- [ ] 数据统计报表

### 第四阶段：移动端优化和测试（3天）
- [ ] 响应式设计
- [ ] 移动端适配
- [ ] 功能测试
- [ ] 性能优化

## 预算分配
- 前端开发：3000元
- 后端开发：3000元  
- 数据库设计：1000元
- 测试优化：1000元

## 技术选型
- 前端：Vue.js 3 + Element Plus + Vite
- 后端：ThinkPHP 6.0
- 数据库：MySQL 8.0
- UI框架：Element Plus（桌面端） + Vant（移动端）