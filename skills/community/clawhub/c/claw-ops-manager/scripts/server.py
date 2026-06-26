#!/usr/bin/env python3
"""
Web UI server for the Audit Center
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)

DB_PATH = Path.home() / ".openclaw" / "audit.db"

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Basic stats
    cursor.execute("SELECT COUNT(*) as count FROM operations")
    total_ops = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM operations WHERE success = 0")
    failed_ops = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM audit_alerts WHERE resolved = 0")
    unresolved_alerts = cursor.fetchone()["count"]

    # Last 24h activity
    since = datetime.now() - timedelta(hours=24)
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM operations
        WHERE timestamp >= ?
    """, (since.isoformat(),))
    recent_activity = cursor.fetchone()["count"]

    # Top tools
    cursor.execute("""
        SELECT tool_name, COUNT(*) as count
        FROM operations
        GROUP BY tool_name
        ORDER BY count DESC
        LIMIT 10
    """)
    top_tools = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        "total_operations": total_ops,
        "failed_operations": failed_ops,
        "unresolved_alerts": unresolved_alerts,
        "recent_24h": recent_activity,
        "top_tools": top_tools
    })

@app.route('/api/operations')
def get_operations():
    """Get operations with filters"""
    conn = get_db_connection()
    cursor = conn.cursor()

    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    tool_name = request.args.get('tool')
    success = request.args.get('success')

    query = "SELECT * FROM operations WHERE 1=1"
    params = []

    if tool_name:
        query += " AND tool_name = ?"
        params.append(tool_name)

    if success is not None:
        query += " AND success = ?"
        params.append(success == 'true')

    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    operations = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(operations)

@app.route('/api/operations/<int:operation_id>')
def get_operation_detail(operation_id):
    """Get detailed information about an operation"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM operations WHERE id = ?", (operation_id,))
    operation = dict(cursor.fetchone())

    # Get related file changes
    cursor.execute("""
        SELECT * FROM file_changes
        WHERE operation_id = ?
        ORDER BY timestamp
    """, (operation_id,))
    file_changes = [dict(row) for row in cursor.fetchall()]

    operation["file_changes"] = file_changes

    conn.close()

    return jsonify(operation)

@app.route('/api/alerts')
def get_alerts():
    """Get audit alerts"""
    conn = get_db_connection()
    cursor = conn.cursor()

    resolved = request.args.get('resolved', 'false')

    cursor.execute("""
        SELECT
            a.*,
            o.tool_name,
            o.action
        FROM audit_alerts a
        LEFT JOIN operations o ON a.operation_id = o.id
        WHERE a.resolved = ?
        ORDER BY a.timestamp DESC
    """, (resolved == 'true',))

    alerts = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(alerts)

@app.route('/api/alerts/<int:alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Mark an alert as resolved"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE audit_alerts
        SET resolved = 1
        WHERE id = ?
    """, (alert_id,))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/api/snapshots', methods=['GET', 'POST'])
def snapshots():
    """Get or create snapshots"""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("""
            SELECT * FROM snapshots
            ORDER BY timestamp DESC
        """)
        snapshots = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(snapshots)

    elif request.method == 'POST':
        data = request.json
        cursor.execute("""
            INSERT INTO snapshots (name, description, snapshot_data, created_by)
            VALUES (?, ?, ?, ?)
        """, (
            data.get('name'),
            data.get('description'),
            json.dumps(data.get('snapshot_data', {})),
            data.get('created_by', 'system')
        ))

        conn.commit()
        snapshot_id = cursor.lastrowid
        conn.close()

        return jsonify({"id": snapshot_id, "success": True})

@app.route('/api/permissions/rules')
def get_permission_rules():
    """Get permission rules"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM permission_rules
        ORDER BY priority DESC
    """)
    rules = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(rules)

@app.route('/api/permissions/check', methods=['POST'])
def check_permission():
    """Check if an operation is allowed"""
    data = request.json
    tool_name = data.get('tool_name')
    action = data.get('action')
    path = data.get('path')

    # Import logger and check permission
    from logger import OperationLogger
    logger = OperationLogger()
    allowed, rule = logger.check_permission(tool_name, action, path)

    return jsonify({
        "allowed": allowed,
        "rule": rule
    })

@app.route('/api/charts/activity')
def activity_chart():
    """Generate activity chart data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Last 7 days
    since = datetime.now() - timedelta(days=7)

    cursor.execute("""
        SELECT
            DATE(timestamp) as date,
            COUNT(*) as count
        FROM operations
        WHERE timestamp >= ?
        GROUP BY DATE(timestamp)
        ORDER BY date
    """, (since.isoformat(),))

    data = cursor.fetchall()
    conn.close()

    dates = [row["date"] for row in data]
    counts = [row["count"] for row in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=counts,
        mode='lines+markers',
        name='Operations',
        line=dict(color='#00ff9f', width=2)
    ))

    fig.update_layout(
        title="Activity (Last 7 Days)",
        xaxis_title="Date",
        yaxis_title="Operations",
        template="plotly_dark",
        height=300
    )

    return jsonify(json.loads(fig.to_json()))

if __name__ == '__main__':
    print("🚀 Starting Audit Center Web UI...")
    print(f"📊 Dashboard: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
