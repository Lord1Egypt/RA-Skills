#!/bin/bash
#
# Mock Server 启动工具 - 本地 API 模拟服务
#
# 用法: bash scripts/mock-server.sh [命令] [选项]
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️${NC}  $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
step() { echo -e "${CYAN}▶ $1${NC}"; }

MOCK_DIR="mock"
PORT=3000
PID_FILE=".mock-server.pid"

# 显示帮助
show_help() {
    echo "Mock Server 启动工具"
    echo ""
    echo "用法: bash scripts/mock-server.sh <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  start        启动 Mock Server"
    echo "  stop         停止 Mock Server"
    echo "  restart      重启 Mock Server"
    echo "  status       查看服务状态"
    echo "  init         初始化 Mock 数据"
    echo "  add <path>   添加新的 API 端点"
    echo ""
    echo "选项:"
    echo "  --port       指定端口 (默认: 3000)"
    echo "  --delay      添加响应延迟(ms)"
    echo ""
}

# 检查依赖
check_deps() {
    if ! command -v node &> /dev/null; then
        error "需要 Node.js 环境"
        info "请安装 Node.js: https://nodejs.org"
        exit 1
    fi
}

# 初始化 Mock 目录
init_mock() {
    step "初始化 Mock 服务器..."

    mkdir -p "$MOCK_DIR/routes"
    mkdir -p "$MOCK_DIR/data"

    # 创建 package.json
    if [ ! -f "$MOCK_DIR/package.json" ]; then
        cat > "$MOCK_DIR/package.json" << 'EOF'
{
  "name": "appdev-mock-server",
  "version": "1.0.0",
  "description": "本地 API Mock 服务",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "body-parser": "^1.20.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
EOF
        success "创建 package.json"
    fi

    # 创建主服务器文件
    if [ ! -f "$MOCK_DIR/server.js" ]; then
        cat > "$MOCK_DIR/server.js" << 'EOF'
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.MOCK_PORT || 3000;
const DELAY = parseInt(process.env.MOCK_DELAY) || 0;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 日志中间件
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
});

// 延迟中间件
app.use((req, res, next) => {
    if (DELAY > 0) {
        setTimeout(next, DELAY);
    } else {
        next();
    }
});

// 加载所有路由
const routesDir = path.join(__dirname, 'routes');
if (fs.existsSync(routesDir)) {
    fs.readdirSync(routesDir).forEach(file => {
        if (file.endsWith('.js')) {
            const route = require(path.join(routesDir, file));
            if (typeof route === 'function') {
                route(app);
                console.log(`✅ 加载路由: ${file}`);
            }
        }
    });
}

// 健康检查
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 404 处理
app.use((req, res) => {
    res.status(404).json({
        error: 'Not Found',
        message: `未找到接口: ${req.method} ${req.url}`,
        available: ['/health', '/api']
    });
});

app.listen(PORT, () => {
    console.log(`
╔══════════════════════════════════════════════════╗
║     🚀 Mock Server 启动成功                      ║
║                                                  ║
║     地址: http://localhost:${PORT}                    ║
║     延迟: ${DELAY}ms                                   ║
╚══════════════════════════════════════════════════╝
`);
});
EOF
        success "创建 server.js"
    fi

    # 创建示例路由
    create_sample_routes

    # 创建示例数据
    create_sample_data

    echo ""
    step "安装依赖..."
    cd "$MOCK_DIR"
    npm install
    cd ..

    echo ""
    success "Mock Server 初始化完成！"
    info "启动命令: bash scripts/mock-server.sh start"
}

# 创建示例路由
create_sample_routes() {
    mkdir -p "$MOCK_DIR/routes"

    # 用户相关 API
    cat > "$MOCK_DIR/routes/user.js" << 'EOF'
const fs = require('fs');
const path = require('path');

const dataFile = path.join(__dirname, '../data/users.json');

function loadData() {
    if (fs.existsSync(dataFile)) {
        return JSON.parse(fs.readFileSync(dataFile, 'utf8'));
    }
    return [];
}

function saveData(data) {
    fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));
}

module.exports = function(app) {
    // 获取用户列表
    app.get('/api/users', (req, res) => {
        const { page = 1, size = 10, keyword } = req.query;
        let data = loadData();

        if (keyword) {
            data = data.filter(u => u.name.includes(keyword));
        }

        const total = data.length;
        const start = (page - 1) * size;
        const list = data.slice(start, start + parseInt(size));

        res.json({
            code: 0,
            data: {
                list,
                total,
                page: parseInt(page),
                size: parseInt(size),
                hasMore: start + list.length < total
            }
        });
    });

    // 获取单个用户
    app.get('/api/users/:id', (req, res) => {
        const data = loadData();
        const user = data.find(u => u.id === req.params.id);

        if (user) {
            res.json({ code: 0, data: user });
        } else {
            res.status(404).json({ code: 404, error: '用户不存在' });
        }
    });

    // 创建用户
    app.post('/api/users', (req, res) => {
        const data = loadData();
        const newUser = {
            id: Date.now().toString(),
            ...req.body,
            createdAt: new Date().toISOString()
        };

        data.push(newUser);
        saveData(data);

        res.status(201).json({ code: 0, data: newUser });
    });

    // 更新用户
    app.put('/api/users/:id', (req, res) => {
        const data = loadData();
        const index = data.findIndex(u => u.id === req.params.id);

        if (index !== -1) {
            data[index] = { ...data[index], ...req.body, updatedAt: new Date().toISOString() };
            saveData(data);
            res.json({ code: 0, data: data[index] });
        } else {
            res.status(404).json({ code: 404, error: '用户不存在' });
        }
    });

    // 删除用户
    app.delete('/api/users/:id', (req, res) => {
        const data = loadData();
        const index = data.findIndex(u => u.id === req.params.id);

        if (index !== -1) {
            const deleted = data.splice(index, 1)[0];
            saveData(data);
            res.json({ code: 0, data: deleted });
        } else {
            res.status(404).json({ code: 404, error: '用户不存在' });
        }
    });
};
EOF

    # 认证相关 API
    cat > "$MOCK_DIR/routes/auth.js" << 'EOF'
module.exports = function(app) {
    // 登录
    app.post('/api/auth/login', (req, res) => {
        const { username, password } = req.body;

        // 模拟验证
        if (username === 'admin' && password === 'admin') {
            res.json({
                code: 0,
                data: {
                    token: 'mock_token_' + Date.now(),
                    user: {
                        id: '1',
                        username: 'admin',
                        name: '管理员'
                    }
                }
            });
        } else {
            res.status(401).json({
                code: 401,
                error: '用户名或密码错误'
            });
        }
    });

    // 登出
    app.post('/api/auth/logout', (req, res) => {
        res.json({ code: 0, message: '登出成功' });
    });

    // 获取当前用户
    app.get('/api/auth/me', (req, res) => {
        res.json({
            code: 0,
            data: {
                id: '1',
                username: 'admin',
                name: '管理员'
            }
        });
    });
};
EOF

    success "创建示例路由"
}

# 创建示例数据
create_sample_data() {
    mkdir -p "$MOCK_DIR/data"

    cat > "$MOCK_DIR/data/users.json" << 'EOF'
[
  {
    "id": "1",
    "name": "张三",
    "email": "zhangsan@example.com",
    "phone": "13800138001",
    "status": "active",
    "createdAt": "2024-01-01T00:00:00Z"
  },
  {
    "id": "2",
    "name": "李四",
    "email": "lisi@example.com",
    "phone": "13800138002",
    "status": "active",
    "createdAt": "2024-01-02T00:00:00Z"
  },
  {
    "id": "3",
    "name": "王五",
    "email": "wangwu@example.com",
    "phone": "13800138003",
    "status": "inactive",
    "createdAt": "2024-01-03T00:00:00Z"
  }
]
EOF

    success "创建示例数据"
}

# 启动服务
start_server() {
    step "启动 Mock Server..."
    check_deps

    if [ ! -d "$MOCK_DIR" ]; then
        init_mock
    fi

    # 检查是否已在运行
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            warn "Mock Server 已在运行 (PID: $pid)"
            info "访问: http://localhost:$PORT"
            return
        fi
    fi

    # 启动服务
    cd "$MOCK_DIR"
    MOCK_PORT=$PORT MOCK_DELAY=${DELAY:-0} nohup node server.js > ../mock-server.log 2>&1 &
    local server_pid=$!
    cd ..

    echo $server_pid > "$PID_FILE"

    # 等待启动
    sleep 2

    if kill -0 "$server_pid" 2>/dev/null; then
        success "Mock Server 启动成功！"
        info "访问地址: http://localhost:$PORT"
        info "日志文件: mock-server.log"
        echo ""
        info "可用接口:"
        info "  GET    http://localhost:$PORT/health"
        info "  GET    http://localhost:$PORT/api/users"
        info "  POST   http://localhost:$PORT/api/auth/login"
    else
        error "启动失败，查看 mock-server.log"
        rm -f "$PID_FILE"
        exit 1
    fi
}

# 停止服务
stop_server() {
    step "停止 Mock Server..."

    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            rm -f "$PID_FILE"
            success "Mock Server 已停止"
        else
            warn "服务未在运行"
            rm -f "$PID_FILE"
        fi
    else
        warn "未找到 PID 文件"
    fi
}

# 查看状态
show_status() {
    step "Mock Server 状态"

    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            success "服务运行中 (PID: $pid)"
            info "访问: http://localhost:$PORT"

            # 测试健康检查
            if command -v curl &> /dev/null; then
                echo ""
                info "健康检查:"
                curl -s http://localhost:$PORT/health | head -1 || warn "无法连接"
            fi
        else
            error "服务未运行 (PID 文件存在但进程不存在)"
            rm -f "$PID_FILE"
        fi
    else
        info "服务未运行"
    fi

    if [ -f "mock-server.log" ]; then
        echo ""
        info "最近日志:"
        tail -5 mock-server.log 2>/dev/null || true
    fi
}

# 添加新端点
add_endpoint() {
    local path="$1"
    if [ -z "$path" ]; then
        error "请指定端点路径"
        info "示例: bash scripts/mock-server.sh add product"
        exit 1
    fi

    step "添加新端点: $path"

    if [ ! -d "$MOCK_DIR" ]; then
        init_mock
    fi

    # 创建路由文件
    cat > "$MOCK_DIR/routes/$path.js" << EOF
module.exports = function(app) {
    // GET /api/$path
    app.get('/api/$path', (req, res) => {
        res.json({
            code: 0,
            data: {
                message: '$path 列表',
                list: []
            }
        });
    });

    // GET /api/$path/:id
    app.get('/api/$path/:id', (req, res) => {
        res.json({
            code: 0,
            data: {
                id: req.params.id,
                name: '示例数据'
            }
        });
    });

    // POST /api/$path
    app.post('/api/$path', (req, res) => {
        res.status(201).json({
            code: 0,
            data: {
                id: Date.now().toString(),
                ...req.body
            }
        });
    });

    // PUT /api/$path/:id
    app.put('/api/$path/:id', (req, res) => {
        res.json({
            code: 0,
            data: {
                id: req.params.id,
                ...req.body
            }
        });
    });

    // DELETE /api/$path/:id
    app.delete('/api/$path/:id', (req, res) => {
        res.json({ code: 0, message: '删除成功' });
    });
};
EOF

    success "路由文件已创建: mock/routes/$path.js"
    info "服务重启后生效"
}

# 主函数
main() {
    local cmd="${1:-status}"
    shift || true

    # 解析选项
    while [[ $# -gt 0 ]]; do
        case $1 in
            --port=*)
                PORT="${1#*=}"
                shift
                ;;
            --delay=*)
                DELAY="${1#*=}"
                shift
                ;;
            *)
                shift
                ;;
        esac
    done

    case "$cmd" in
        start)
            start_server
            ;;
        stop)
            stop_server
            ;;
        restart)
            stop_server
            sleep 1
            start_server
            ;;
        status)
            show_status
            ;;
        init)
            init_mock
            ;;
        add)
            add_endpoint "$1"
            ;;
        --help|-h)
            show_help
            ;;
        *)
            error "未知命令: $cmd"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
