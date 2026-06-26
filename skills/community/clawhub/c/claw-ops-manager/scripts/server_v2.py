#!/usr/bin/env python3
"""
Full-featured Web UI with complete management interface
Uses only Python standard library for compatibility
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import os
import subprocess
import hashlib

DB_PATH = Path.home() / ".openclaw" / "audit.db"
CONFIG_PATH = Path.home() / ".openclaw" / "audit-config.json"

class AuditAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.directory = Path(__file__).parent
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == '/' or parsed.path == '/index.html':
            self.serve_main_app()
        elif parsed.path.startswith('/api/'):
            self.handle_api_get(parsed)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith('/api/'):
            self.handle_api_post(parsed)
        else:
            self.send_error(404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith('/api/'):
            self.handle_api_delete(parsed)
        else:
            self.send_error(404)

    def serve_main_app(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        try:
            self.wfile.write(self.get_full_app_html_v2().encode('utf-8'))
        except:
            self.wfile.write(self.get_full_app_html().encode('utf-8'))

    def get_full_app_html_v2(self):
        """加载 v2 dashboard"""
        dashboard_path = Path(__file__).parent.parent / "assets" / "templates" / "dashboard_v2.html"
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            return f.read()

    def get_full_app_html(self):
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claw 运营管理中心</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
        }

        .header {
            background: white;
            border-radius: 12px;
            padding: 25px 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            color: #667eea;
            font-size: 28px;
            font-weight: 700;
        }

        .header-controls {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }

        .refresh-btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }

        .stat-label {
            color: #999;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .stat-value {
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .main-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        @media (max-width: 1200px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        .panel {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }

        .panel-title {
            font-size: 20px;
            font-weight: 700;
            color: #333;
        }

        .filters {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .filter-input, .filter-select {
            padding: 8px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
        }

        .filter-input:focus, .filter-select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .filter-input {
            flex: 1;
            min-width: 200px;
        }

        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            font-size: 14px;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover {
            background: #5568d3;
        }

        .btn-success {
            background: #10b981;
            color: white;
        }

        .btn-success:hover {
            background: #059669;
        }

        .btn-danger {
            background: #ef4444;
            color: white;
        }

        .btn-danger:hover {
            background: #dc2626;
        }

        .btn-sm {
            padding: 5px 12px;
            font-size: 12px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #e0e0e0;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #f0f0f0;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .badge-success {
            background: #d1fae5;
            color: #065f46;
        }

        .badge-danger {
            background: #fee2e2;
            color: #991b1b;
        }

        .badge-warning {
            background: #fef3c7;
            color: #92400e;
        }

        .badge-info {
            background: #dbeafe;
            color: #1e40af;
        }

        .alert-item {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 8px;
        }

        .alert-item.high {
            background: #fee2e2;
            border-left-color: #ef4444;
        }

        .alert-item.medium {
            background: #fef3c7;
            border-left-color: #f59e0b;
        }

        .alert-item.low {
            background: #dbeafe;
            border-left-color: #3b82f6;
        }

        .alert-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .alert-type {
            font-weight: 700;
            color: #92400e;
        }

        .alert-item.high .alert-type {
            color: #991b1b;
        }

        .alert-item.low .alert-type {
            color: #1e40af;
        }

        .alert-message {
            color: #666;
            font-size: 14px;
        }

        .alert-time {
            font-size: 12px;
            color: #999;
            margin-top: 8px;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .empty-state-icon {
            font-size: 64px;
            margin-bottom: 20px;
            opacity: 0.3;
        }

        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }

        .tab {
            padding: 12px 20px;
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
        }

        .tab:hover {
            color: #667eea;
        }

        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .code-block {
            background: #1e293b;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            overflow-x: auto;
            margin: 10px 0;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            border-radius: 12px;
            padding: 30px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }

        .modal-title {
            font-size: 20px;
            font-weight: 700;
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #999;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }

        .form-input, .form-textarea, .form-select {
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
        }

        .form-input:focus, .form-textarea:focus, .form-select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .form-textarea {
            min-height: 100px;
            resize: vertical;
        }

        .pagination {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }

        .pagination button {
            padding: 8px 12px;
            border: 1px solid #e0e0e0;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .pagination button:hover {
            background: #f0f0f0;
        }

        .pagination button.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        .snapshot-list {
            display: grid;
            gap: 15px;
        }

        .snapshot-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s;
        }

        .snapshot-item:hover {
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .snapshot-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .snapshot-name {
            font-weight: 700;
            font-size: 16px;
            color: #333;
        }

        .snapshot-time {
            font-size: 12px;
            color: #999;
        }

        .snapshot-description {
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }

        .snapshot-actions {
            display: flex;
            gap: 10px;
        }

        .rule-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin-bottom: 12px;
        }

        .rule-item.denied {
            border-left-color: #ef4444;
        }

        .rule-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .rule-name {
            font-weight: 700;
            color: #333;
        }

        .rule-patterns {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }

        .rule-pattern {
            background: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-family: monospace;
            color: #666;
        }

        .loading-spinner {
            text-align: center;
            padding: 40px;
            color: #999;
        }

        .loading-spinner::after {
            content: "⏳";
            font-size: 48px;
            display: block;
            margin-bottom: 20px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .auto-refresh-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #10b981;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Claw 运营管理中心</h1>
            <div class="header-controls">
                <span style="color: #999; font-size: 14px;">
                    <span class="auto-refresh-indicator"></span>
                    自动刷新中
                </span>
                <button class="refresh-btn" onclick="refreshAll()">🔄 刷新</button>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">总操作数</div>
                <div class="stat-value" id="total-ops">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">失败操作</div>
                <div class="stat-value" id="failed-ops">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">未解决告警</div>
                <div class="stat-value" id="unresolved-alerts">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">24小时活动</div>
                <div class="stat-value" id="recent-activity">-</div>
            </div>
        </div>

        <div class="main-grid">
            <div class="panel">
                <div class="tabs">
                    <button class="tab active" onclick="switchTab('operations')">📋 操作记录</button>
                    <button class="tab" onclick="switchTab('snapshots')">📸 快照管理</button>
                    <button class="tab" onclick="switchTab('permissions')">🔒 权限管理</button>
                </div>

                <div id="tab-operations" class="tab-content active">
                    <div class="panel-header">
                        <div class="panel-title">操作记录</div>
                    </div>

                    <div class="filters">
                        <input type="text" class="filter-input" id="search-filter" placeholder="🔍 搜索操作..." onkeyup="filterOperations()">
                        <select class="filter-select" id="tool-filter" onchange="filterOperations()">
                            <option value="">所有工具</option>
                        </select>
                        <select class="filter-select" id="status-filter" onchange="filterOperations()">
                            <option value="">所有状态</option>
                            <option value="success">成功</option>
                            <option value="failed">失败</option>
                        </select>
                        <input type="datetime-local" class="filter-input" id="date-from" onchange="filterOperations()">
                        <input type="datetime-local" class="filter-input" id="date-to" onchange="filterOperations()">
                    </div>

                    <div id="operations-table"></div>
                </div>

                <div id="tab-snapshots" class="tab-content">
                    <div class="panel-header">
                        <div class="panel-title">快照管理</div>
                        <button class="btn btn-primary btn-sm" onclick="showCreateSnapshotModal()">+ 创建快照</button>
                    </div>

                    <div id="snapshots-list"></div>
                </div>

                <div id="tab-permissions" class="tab-content">
                    <div class="panel-header">
                        <div class="panel-title">权限规则</div>
                        <button class="btn btn-primary btn-sm" onclick="showCreateRuleModal()">+ 添加规则</button>
                    </div>

                    <div id="rules-list"></div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">🚨 活跃告警</div>
                </div>
                <div id="alerts-list"></div>
            </div>
        </div>
    </div>

    <!-- 创建快照模态框 -->
    <div id="create-snapshot-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">创建快照</div>
                <button class="close-btn" onclick="closeModal('create-snapshot-modal')">&times;</button>
            </div>
            <form onsubmit="createSnapshot(event)">
                <div class="form-group">
                    <label class="form-label">快照名称</label>
                    <input type="text" class="form-input" id="snapshot-name" required placeholder="例如: upgrade-before">
                </div>
                <div class="form-group">
                    <label class="form-label">描述</label>
                    <textarea class="form-textarea" id="snapshot-description" placeholder="快照的详细描述..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary">创建快照</button>
            </form>
        </div>
    </div>

    <!-- 创建规则模态框 -->
    <div id="create-rule-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">添加权限规则</div>
                <button class="close-btn" onclick="closeModal('create-rule-modal')">&times;</button>
            </div>
            <form onsubmit="createRule(event)">
                <div class="form-group">
                    <label class="form-label">规则名称</label>
                    <input type="text" class="form-input" id="rule-name" required placeholder="例如: protect-ssh">
                </div>
                <div class="form-group">
                    <label class="form-label">工具模式</label>
                    <input type="text" class="form-input" id="rule-tool" required placeholder="例如: exec, write, *">
                </div>
                <div class="form-group">
                    <label class="form-label">操作模式</label>
                    <input type="text" class="form-input" id="rule-action" required placeholder="例如: *, run_command">
                </div>
                <div class="form-group">
                    <label class="form-label">路径模式</label>
                    <input type="text" class="form-input" id="rule-path" required placeholder="例如: /etc/*, ~/.ssh/*">
                </div>
                <div class="form-group">
                    <label class="form-label">是否允许</label>
                    <select class="form-select" id="rule-allowed">
                        <option value="true">允许</option>
                        <option value="false">拒绝</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">优先级 (0-100)</label>
                    <input type="number" class="form-input" id="rule-priority" value="50" min="0" max="100">
                </div>
                <button type="submit" class="btn btn-primary">添加规则</button>
            </form>
        </div>
    </div>

    <script>
        let allOperations = [];
        let currentPage = 1;
        const itemsPerPage = 20;

        // 页面加载
        document.addEventListener('DOMContentLoaded', function() {
            refreshAll();
            setInterval(refreshAll, 30000); // 每30秒自动刷新
        });

        // 切换标签
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

            event.target.classList.add('active');
            document.getElementById('tab-' + tabName).classList.add('active');

            if (tabName === 'snapshots') loadSnapshots();
            if (tabName === 'permissions') loadRules();
        }

        // 刷新所有数据
        async function refreshAll() {
            await Promise.all([
                loadStats(),
                loadOperations(),
                loadAlerts()
            ]);
        }

        // 加载统计数据
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();

                document.getElementById('total-ops').textContent = stats.total_operations.toLocaleString();
                document.getElementById('failed-ops').textContent = stats.failed_operations.toLocaleString();
                document.getElementById('unresolved-alerts').textContent = stats.unresolved_alerts.toLocaleString();
                document.getElementById('recent-activity').textContent = stats.recent_24h.toLocaleString();
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }

        // 加载操作记录
        async function loadOperations() {
            try {
                const response = await fetch('/api/operations?limit=1000');
                allOperations = await response.json();

                populateToolFilter();
                displayOperations();
            } catch (error) {
                console.error('Error loading operations:', error);
            }
        }

        // 填充工具过滤器
        function populateToolFilter() {
            const tools = [...new Set(allOperations.map(op => op.tool_name))].sort();
            const select = document.getElementById('tool-filter');
            select.innerHTML = '<option value="">所有工具</option>' +
                tools.map(t => `<option value="${t}">${t}</option>`).join('');
        }

        // 筛选操作
        function filterOperations() {
            const search = document.getElementById('search-filter').value.toLowerCase();
            const tool = document.getElementById('tool-filter').value;
            const status = document.getElementById('status-filter').value;
            const dateFrom = document.getElementById('date-from').value;
            const dateTo = document.getElementById('date-to').value;

            allOperations = allOperations.filter(op => {
                if (search && !op.action.toLowerCase().includes(search)) return false;
                if (tool && op.tool_name !== tool) return false;
                if (status === 'success' && !op.success) return false;
                if (status === 'failed' && op.success) return false;
                if (dateFrom && new Date(op.timestamp) < new Date(dateFrom)) return false;
                if (dateTo && new Date(op.timestamp) > new Date(dateTo)) return false;
                return true;
            });

            currentPage = 1;
            displayOperations();
        }

        // 显示操作记录
        function displayOperations() {
            const container = document.getElementById('operations-table');
            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const pageData = allOperations.slice(start, end);

            if (pageData.length === 0) {
                container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📭</div><p>暂无操作记录</p></div>';
                return;
            }

            let html = `
                <table>
                    <thead>
                        <tr>
                            <th>时间</th>
                            <th>工具</th>
                            <th>操作</th>
                            <th>状态</th>
                            <th>耗时</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            pageData.forEach(op => {
                const time = new Date(op.timestamp).toLocaleString('zh-CN');
                const status = op.success ?
                    '<span class="badge badge-success">✓ 成功</span>' :
                    '<span class="badge badge-danger">✗ 失败</span>';

                html += `
                    <tr>
                        <td><small>${time}</small></td>
                        <td><code>${op.tool_name}</code></td>
                        <td>${op.action}</td>
                        <td>${status}</td>
                        <td>${op.duration_ms}ms</td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="viewOperationDetails(${op.id})">详情</button>
                        </td>
                    </tr>
                `;
            });

            html += '</tbody></table>';

            // 分页
            const totalPages = Math.ceil(allOperations.length / itemsPerPage);
            if (totalPages > 1) {
                html += '<div class="pagination">';
                for (let i = 1; i <= totalPages; i++) {
                    html += `<button class="${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
                }
                html += '</div>';
            }

            container.innerHTML = html;
        }

        // 跳转页面
        function goToPage(page) {
            currentPage = page;
            displayOperations();
            document.querySelector('.panel').scrollTop = 0;
        }

        // 查看操作详情
        async function viewOperationDetails(id) {
            try {
                const response = await fetch(`/api/operations/${id}`);
                const op = await response.json();

                alert(`操作详情:\\n\\n工具: ${op.tool_name}\\n操作: ${op.action}\\n参数: ${op.parameters}\\n结果: ${op.result}\\n状态: ${op.success ? '成功' : '失败'}\\n耗时: ${op.duration_ms}ms`);
            } catch (error) {
                console.error('Error loading operation details:', error);
            }
        }

        // 加载告警
        async function loadAlerts() {
            try {
                const response = await fetch('/api/alerts?resolved=false');
                const alerts = await response.json();

                const container = document.getElementById('alerts-list');

                if (alerts.length === 0) {
                    container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">✅</div><p>暂无活跃告警</p></div>';
                    return;
                }

                let html = '';
                alerts.forEach(alert => {
                    const time = new Date(alert.timestamp).toLocaleString('zh-CN');
                    const severityClass = alert.severity || 'medium';

                    html += `
                        <div class="alert-item ${severityClass}">
                            <div class="alert-header">
                                <div class="alert-type">${alert.alert_type}</div>
                                <button class="btn btn-sm btn-success" onclick="resolveAlert(${alert.id})">解决</button>
                            </div>
                            <div class="alert-message">${alert.message}</div>
                            <div class="alert-time">${time}</div>
                        </div>
                    `;
                });

                container.innerHTML = html;
            } catch (error) {
                console.error('Error loading alerts:', error);
            }
        }

        // 解决告警
        async function resolveAlert(id) {
            try {
                await fetch(`/api/alerts/${id}/resolve`, { method: 'POST' });
                loadAlerts();
                loadStats();
            } catch (error) {
                console.error('Error resolving alert:', error);
            }
        }

        // 加载快照
        async function loadSnapshots() {
            try {
                const response = await fetch('/api/snapshots');
                const snapshots = await response.json();

                const container = document.getElementById('snapshots-list');

                if (snapshots.length === 0) {
                    container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📸</div><p>暂无快照</p></div>';
                    return;
                }

                let html = '<div class="snapshot-list">';
                snapshots.forEach(snap => {
                    const time = new Date(snap.timestamp).toLocaleString('zh-CN');

                    html += `
                        <div class="snapshot-item">
                            <div class="snapshot-header">
                                <div class="snapshot-name">${snap.name}</div>
                                <button class="btn btn-sm btn-danger" onclick="deleteSnapshot(${snap.id})">删除</button>
                            </div>
                            <div class="snapshot-time">${time}</div>
                            <div class="snapshot-description">${snap.description || '无描述'}</div>
                            <div class="snapshot-actions">
                                <button class="btn btn-sm btn-primary" onclick="compareSnapshot(${snap.id})">对比</button>
                                <button class="btn btn-sm btn-success" onclick="restoreSnapshot(${snap.id})">恢复</button>
                            </div>
                        </div>
                    `;
                });
                html += '</div>';

                container.innerHTML = html;
            } catch (error) {
                console.error('Error loading snapshots:', error);
            }
        }

        // 加载权限规则
        async function loadRules() {
            try {
                const response = await fetch('/api/permissions/rules');
                const rules = await response.json();

                const container = document.getElementById('rules-list');

                if (rules.length === 0) {
                    container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🔒</div><p>暂无权限规则</p></div>';
                    return;
                }

                let html = '';
                rules.forEach(rule => {
                    const allowedClass = rule.allowed ? '' : 'denied';

                    html += `
                        <div class="rule-item ${allowedClass}">
                            <div class="rule-header">
                                <div class="rule-name">${rule.rule_name}</div>
                                <button class="btn btn-sm btn-danger" onclick="deleteRule(${rule.id})">删除</button>
                            </div>
                            <div class="rule-patterns">
                                <span class="rule-pattern">工具: ${rule.tool_pattern}</span>
                                <span class="rule-pattern">操作: ${rule.action_pattern}</span>
                                <span class="rule-pattern">路径: ${rule.path_pattern}</span>
                                <span class="rule-pattern">优先级: ${rule.priority}</span>
                            </div>
                            <div>
                                <span class="badge ${rule.allowed ? 'badge-success' : 'badge-danger'}">
                                    ${rule.allowed ? '✓ 允许' : '✗ 拒绝'}
                                </span>
                            </div>
                        </div>
                    `;
                });

                container.innerHTML = html;
            } catch (error) {
                console.error('Error loading rules:', error);
            }
        }

        // 创建快照
        async function createSnapshot(event) {
            event.preventDefault();

            const name = document.getElementById('snapshot-name').value;
            const description = document.getElementById('snapshot-description').value;

            try {
                const response = await fetch('/api/snapshots', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: name,
                        description: description
                    })
                });

                if (response.ok) {
                    closeModal('create-snapshot-modal');
                    loadSnapshots();
                    alert('✅ 快照创建成功！');
                }
            } catch (error) {
                console.error('Error creating snapshot:', error);
                alert('❌ 创建快照失败');
            }
        }

        // 创建规则
        async function createRule(event) {
            event.preventDefault();

            const rule = {
                rule_name: document.getElementById('rule-name').value,
                tool_pattern: document.getElementById('rule-tool').value,
                action_pattern: document.getElementById('rule-action').value,
                path_pattern: document.getElementById('rule-path').value,
                allowed: document.getElementById('rule-allowed').value === 'true',
                priority: parseInt(document.getElementById('rule-priority').value)
            };

            try {
                const response = await fetch('/api/permissions/rules', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(rule)
                });

                if (response.ok) {
                    closeModal('create-rule-modal');
                    loadRules();
                    alert('✅ 规则添加成功！');
                }
            } catch (error) {
                console.error('Error creating rule:', error);
                alert('❌ 添加规则失败');
            }
        }

        // 删除快照
        async function deleteSnapshot(id) {
            if (!confirm('确定要删除这个快照吗？')) return;

            try {
                await fetch(`/api/snapshots/${id}`, { method: 'DELETE' });
                loadSnapshots();
            } catch (error) {
                console.error('Error deleting snapshot:', error);
            }
        }

        // 删除规则
        async function deleteRule(id) {
            if (!confirm('确定要删除这个规则吗？')) return;

            try {
                await fetch(`/api/permissions/rules/${id}`, { method: 'DELETE' });
                loadRules();
            } catch (error) {
                console.error('Error deleting rule:', error);
            }
        }

        // 恢复快照
        async function restoreSnapshot(id) {
            if (!confirm('确定要恢复到这个快照吗？\\n\\n注意：此功能需要集成备份系统（git/restic/rsync）')) return;

            try {
                const response = await fetch(`/api/snapshots/${id}/restore`, {
                    method: 'POST'
                });
                const result = await response.json();

                if (result.requires_backup) {
                    alert('⚠️ 恢复功能需要集成备份系统。\\n\\n请配置 git、restic 或 rsync 来实现真实的文件恢复。\\n\\n当前快照仅包含元数据和哈希值。');
                }
            } catch (error) {
                console.error('Error restoring snapshot:', error);
            }
        }

        // 对比快照
        async function compareSnapshot(id) {
            try {
                const response = await fetch(`/api/snapshots/${id}/compare`);
                const diff = await response.json();

                alert(`快照差异:\\n\\n新增文件: ${diff.added.length}\\n删除文件: ${diff.removed.length}\\n修改文件: ${diff.modified.length}`);
            } catch (error) {
                console.error('Error comparing snapshot:', error);
            }
        }

        // 显示模态框
        function showCreateSnapshotModal() {
            document.getElementById('create-snapshot-modal').classList.add('active');
        }

        function showCreateRuleModal() {
            document.getElementById('create-rule-modal').classList.add('active');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }

        // 点击模态框外部关闭
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    this.classList.remove('active');
                }
            });
        });
    </script>
</body>
</html>
        '''

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def get_db_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def handle_api_get(self, parsed):
        path = parsed.path
        query = parsed.query

        if path == '/api/stats':
            self.send_json(self.get_stats())
        elif path == '/api/operations':
            params = urllib.parse.parse_qs(query)
            limit = int(params.get('limit', [50])[0])
            self.send_json(self.get_operations(limit))
        elif path.startswith('/api/operations/'):
            op_id = int(path.split('/')[-1])
            self.send_json(self.get_operation_details(op_id))
        elif path == '/api/alerts':
            params = urllib.parse.parse_qs(query)
            resolved = params.get('resolved', ['false'])[0] == 'true'
            self.send_json(self.get_alerts(resolved))
        elif path == '/api/snapshots':
            self.send_json(self.get_snapshots())
        elif path == '/api/permissions/rules':
            self.send_json(self.get_permission_rules())
        else:
            self.send_error(404)

    def handle_api_post(self, parsed):
        path = parsed.path

        if path.startswith('/api/alerts/') and path.endswith('/resolve'):
            alert_id = int(path.split('/')[-2])
            self.send_json(self.resolve_alert(alert_id))
        elif path == '/api/snapshots':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            self.send_json(self.create_snapshot(data))
        elif path == '/api/permissions/rules':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            self.send_json(self.create_permission_rule(data))
        elif path.endswith('/rollback'):
            snap_id = path.split('/')[-2]
            self.send_json(self.restore_snapshot(snap_id))
        elif path.endswith('/restore'):
            snap_id = int(path.split('/')[-2])
            self.send_json(self.restore_snapshot(snap_id))
        else:
            self.send_error(404)

    def handle_api_delete(self, parsed):
        path = parsed.path

        if path.startswith('/api/snapshots/'):
            snap_id = int(path.split('/')[-2])
            self.send_json(self.delete_snapshot(snap_id))
        elif path.startswith('/api/permissions/rules/'):
            rule_id = int(path.split('/')[-2])
            self.send_json(self.delete_permission_rule(rule_id))
        else:
            self.send_error(404)

    def get_stats(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM operations")
        total = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM operations WHERE success = 0")
        failed = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM audit_alerts WHERE resolved = 0")
        alerts = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(DISTINCT snapshot_id) as count FROM operations WHERE snapshot_id IS NOT NULL")
        snapshots = cursor.fetchone()["count"]

        since = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute("SELECT COUNT(*) as count FROM operations WHERE timestamp >= ?", (since,))
        recent = cursor.fetchone()["count"]

        conn.close()

        return {
            "total_operations": total,
            "failed_operations": failed,
            "unresolved_alerts": alerts,
            "snapshots_count": snapshots,
            "recent_24h": recent
        }

    def get_operations(self, limit=50):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, timestamp, tool_name, action, success, duration_ms,
                   friendly_name, snapshot_id, user
            FROM operations
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result

    def get_operation_details(self, op_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM operations WHERE id = ?", (op_id,))
        operation = dict(cursor.fetchone())

        cursor.execute("""
            SELECT * FROM file_changes
            WHERE operation_id = ?
            ORDER BY timestamp
        """, (op_id,))
        file_changes = [dict(row) for row in cursor.fetchall()]

        operation["file_changes"] = file_changes
        conn.close()
        return operation

    def get_alerts(self, resolved=False):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.*, o.tool_name, o.action
            FROM audit_alerts a
            LEFT JOIN operations o ON a.operation_id = o.id
            WHERE a.resolved = ?
            ORDER BY a.timestamp DESC
        """, (resolved,))

        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result

    def get_snapshots(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM snapshots
            ORDER BY timestamp DESC
        """)

        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result

    def get_permission_rules(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM permission_rules
            ORDER BY priority DESC
        """)

        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result

    def resolve_alert(self, alert_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE audit_alerts SET resolved = 1 WHERE id = ?", (alert_id,))
        conn.commit()
        conn.close()

        return {"success": True}

    def create_snapshot(self, data):
        from rollback import SnapshotManager

        manager = SnapshotManager()
        snap_id = manager.create_snapshot(
            name=data.get('name'),
            description=data.get('description', ''),
            created_by='web-ui'
        )

        return {"success": True, "id": snap_id}

    def create_permission_rule(self, data):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO permission_rules
                (rule_name, tool_pattern, action_pattern, path_pattern, allowed, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['rule_name'],
                data['tool_pattern'],
                data['action_pattern'],
                data['path_pattern'],
                data['allowed'],
                data['priority']
            ))

            conn.commit()
            conn.close()
            return {"success": True}
        except Exception as e:
            conn.close()
            return {"success": False, "error": str(e)}

    def delete_snapshot(self, snap_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM snapshots WHERE id = ?", (snap_id,))
        conn.commit()
        conn.close()

        return {"success": True}

    def delete_permission_rule(self, rule_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM permission_rules WHERE id = ?", (rule_id,))
        conn.commit()
        conn.close()

        return {"success": True}

    def restore_snapshot(self, snap_id):
        from snapshot import SnapshotManager

        try:
            manager = SnapshotManager()
            result = manager.restore_snapshot(snap_id)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    # 确保数据库存在
    if not DB_PATH.exists():
        print("⚠️  数据库不存在，请先运行: python3 scripts/init.py")
        exit(1)

    server = HTTPServer(('0.0.0.0', 8080), AuditAPIHandler)
    print("🚀 Claw 运营管理中心已启动！")
    print(f"📊 访问地址: http://localhost:8080")
    print(f"📱 局域网访问: http://<your-ip>:8080")
    print()
    print("功能特性:")
    print("  ✅ 操作记录查询和筛选")
    print("  ✅ 权限规则管理")
    print("  ✅ 快照创建和管理")
    print("  ✅ 告警查看和处理")
    print("  ✅ 实时统计")
    print()
    server.serve_forever()
