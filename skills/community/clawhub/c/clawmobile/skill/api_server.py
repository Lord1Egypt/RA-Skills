"""
ClawMobile API Server Implementation
Implements HTTP endpoints for AutoX.js server (port 8765)
Based on API-DOCUMENTATION.md specifications
"""

import json
import time
import traceback
from typing import Dict, Any, Callable, Optional
from datetime import datetime


class APIEndpoint:
    """API Endpoint registration and handler"""

    def __init__(self, path: str, method: str = "GET", handler: Callable = None):
        self.path = path
        self.method = method.upper()
        self.handler = handler

    def matches(self, path: str, method: str) -> bool:
        """Check if request matches this endpoint"""
        return (
            self.method == method.upper() and
            (path == self.path or path.startswith(self.path + "/"))
        )


class APIServer:
    """AutoX.js HTTP Server for ClawMobile"""

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.endpoints = []
        self.middleware = []
        self.state = {
            "running": False,
            "current_task": None,
            "uptime": 0,
            "kernel_type": "accessibility",
            "version": "6.5.5.10",
            "start_time": time.time()
        }

        # Register default endpoints
        self._register_default_endpoints()

    def _register_default_endpoints(self):
        """Register default system endpoints"""

        # Status endpoint
        self.register("GET", "/status", self._handle_status)
        self.register("POST", "/check_status", self._handle_check_status)
        self.register("POST", "/stop", self._handle_stop)

        # Task execution endpoint
        self.register("POST", "/execute", self._handle_execute)

    def register(self, method: str, path: str, handler: Callable = None):
        """Register an API endpoint"""
        endpoint = APIEndpoint(path, method, handler)
        self.endpoints.append(endpoint)

    def add_middleware(self, middleware: Callable):
        """Add middleware to request processing pipeline"""
        self.middleware.append(middleware)

    def _handle_status(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle GET /status requests"""
        return {
            "status": "running",
            "version": self.state["version"],
            "uptime": int(time.time() - self.state["start_time"]),
            "kernel_type": self.state["kernel_type"],
            "running": self.state["running"],
            "current_task": self.state["current_task"],
            "supported_kernels": ["accessibility", "coordinate"],
            "features": {
                "recording": False,
                "ai_intervention": False,
                "anti_detection": True,
                "ocr": False
            }
        }

    def _handle_check_status(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle POST /check_status requests"""
        return {
            "running": self.state["running"],
            "current_task": self.state["current_task"],
            "progress": self._get_progress(),
            "uptime": int(time.time() - self.state["start_time"]),
            "kernel_type": self.state["kernel_type"],
            "memory_usage": "45MB",
            "cpu_usage": "12%"
        }

    def _handle_stop(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle POST /stop requests"""
        if self.state["current_task"]:
            self.state["current_task"]["stopped"] = True
            self.state["running"] = False
            return {
                "success": True,
                "message": "Task stopped successfully",
                "stopped_task_id": self.state["current_task"]["id"]
            }
        else:
            return {
                "error": "No task running"
            }

    def _handle_execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle POST /execute requests - Task execution"""
        try:
            task = request.get("body", {})
            task_id = task.get("id")

            if not task_id:
                return {
                    "success": False,
                    "error": "Missing task_id"
                }

            # Set task state
            self.state["running"] = True
            self.state["current_task"] = {
                "id": task_id,
                "workflow_id": task.get("metadata", {}).get("workflow_id"),
                "progress": 0,
                "started_at": datetime.now().isoformat()
            }

            # Validate task
            if not self._validate_task(task):
                return {
                    "success": False,
                    "error": "Invalid task structure"
                }

            # Execute task steps (simplified for MVP)
            result = self._execute_task_steps(task)

            # Update state
            self.state["running"] = False
            self.state["current_task"] = None

            return {
                "success": True,
                "result": result
            }

        except Exception as e:
            self.state["running"] = False
            self.state["current_task"] = None

            return {
                "success": False,
                "error": str(e),
                "stack": traceback.format_exc()
            }

    def _validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate task structure"""
        required_fields = ["id", "steps"]
        for field in required_fields:
            if field not in task:
                return False

        if not isinstance(task.get("steps"), list):
            return False

        return len(task["steps"]) > 0

    def _execute_task_steps(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task steps - MVP implementation"""
        steps_result = []
        total_steps = len(task.get("steps", []))

        for i, step in enumerate(task.get("steps", [])):
            step_id = step.get("step_id", f"step_{i+1:03d}")

            try:
                step_result = self._execute_step(step, step_id)
                steps_result.append(step_result)

                # Update progress
                self.state["current_task"]["progress"] = (i + 1) / total_steps

            except Exception as e:
                steps_result.append({
                    "step_id": step_id,
                    "success": False,
                    "error": str(e)
                })
                raise

        return {
            "task_id": task["id"],
            "status": "completed",
            "steps_result": steps_result,
            "total_duration_ms": 1000,
            "completed_at": datetime.now().isoformat()
        }

    def _execute_step(self, step: Dict[str, Any], step_id: str) -> Dict[str, Any]:
        """Execute a single step - MVP implementation"""
        action = step.get("action")
        start_time = time.time()

        if action == "click":
            return self._execute_click(step, step_id)
        elif action == "input":
            return self._execute_input(step, step_id)
        elif action == "swipe":
            return self._execute_swipe(step, step_id)
        elif action == "wait":
            return self._execute_wait(step, step_id)
        else:
            raise Exception(f"Unknown action: {action}")

    def _execute_click(self, step: Dict[str, Any], step_id: str) -> Dict[str, Any]:
        """Execute click action"""
        return {
            "step_id": step_id,
            "success": True,
            "duration_ms": int((time.time() - start_time) * 1000),
            "action": "click"
        }

    def _execute_input(self, step: Dict[str, Any], step_id: str) -> Dict[str, Any]:
        """Execute input action"""
        value = step.get("value", "")
        return {
            "step_id": step_id,
            "success": True,
            "duration_ms": int((time.time() - start_time) * 1000),
            "value": value
        }

    def _execute_swipe(self, step: Dict[str, Any], step_id: str) -> Dict[str, Any]:
        """Execute swipe action"""
        start = step.get("start", [0, 0])
        end = step.get("end", [0, 0])
        duration = step.get("duration", 300)

        return {
            "step_id": step_id,
            "success": True,
            "duration_ms": duration,
            "start": start,
            "end": end
        }

    def _execute_wait(self, step: Dict[str, Any], step_id: str) -> Dict[str, Any]:
        """Execute wait action"""
        condition = step.get("condition", {})
        timeout = condition.get("timeout", 5000)

        # MVP: Simulate wait
        time.sleep(min(timeout / 1000, 5))

        return {
            "step_id": step_id,
            "success": True,
            "duration_ms": timeout
        }

    def _get_progress(self) -> float:
        """Get current task progress"""
        if self.state["current_task"]:
            return self.state["current_task"].get("progress", 0)
        return 0.0


class MembershipAPI:
    """Membership Management API endpoints"""

    @staticmethod
    def activate_redeem_code(code: str, user_id: str) -> Dict[str, Any]:
        """
        Activate membership using redeem code
        POST /api/v1/membership/redeem
        """
        if not code or not user_id:
            return {
                "success": False,
                "error": "INVALID_CODE",
                "message": "兑换码格式无效"
            }

        # Validate code format
        if not MembershipAPI._validate_code_format(code):
            return {
                "success": False,
                "error": "INVALID_CODE",
                "message": "兑换码格式无效"
            }

        # Parse tier from code
        parts = code.split('-')
        tier_str = parts[0].lower()
        tier = tier_str if tier_str in ["vip", "svip"] else "vip"

        return {
            "success": True,
            "message": "兑换成功！",
            "tier": tier,
            "duration_days": 30,
            "expires_at": "2026-04-30T15:00:00Z"
        }

    @staticmethod
    def _validate_code_format(code: str) -> bool:
        """Validate redeem code format"""
        import re
        pattern = r'^(VIP|SVIP)-\d{4}-[A-Z0-9]{8}$'
        return bool(re.match(pattern, code))

    @staticmethod
    def get_membership_status(user_id: str) -> Dict[str, Any]:
        """
        Get membership status for user
        GET /api/v1/membership/status
        """
        return {
            "success": True,
            "membership": {
                "user_id": user_id,
                "tier": "free",
                "activated_at": None,
                "expires_at": None,
                "activated_code": None,
                "is_test": False,
                "auto_renew": False,
                "payment_source": None,
                "transaction_id": None
            },
            "status": {
                "is_active": False,
                "days_remaining": 0,
                "is_expired": False,
                "will_expire_soon": False
            },
            "permissions": {
                "max_daily_runs": 3,
                "can_export_import": False,
                "can_schedule": False,
                "can_use_ai_intervention": False,
                "can_develop_manually": False,
                "can_use_natural_language": True,
                "priority_support": False
            },
            "today_usage": {
                "runs_completed": 0,
                "runs_remaining": 3,
                "date": datetime.now().strftime('%Y-%m-%d')
            }
        }


# AutoX.js server simulation script generator
def create_autox_server_script() -> str:
    """Generate AutoX.js HTTP server script"""

    script = '''// ClawMobile API Server for AutoX.js v6.5.5.10
// HTTP Server on port 8765

const http = require("http");

const AUTH_TOKEN = "clawmobile-secret-token-change-in-production";
const server_state = {
    running: false,
    current_task: null,
    start_time: Date.now()
};

function authenticate(req) {
    let authHeader = req.headers["authorization"];
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
        return false;
    }
    let token = authHeader.substring(7);
    return token === AUTH_TOKEN;
}

function createResponse(data, statusCode = 200) {
    return JSON.stringify(data);
}

const server = http.createServer((req, res) => {
    console.log("Request:", req.method, req.url);

    // Authentication
    if (!authenticate(req)) {
        res.writeHead(401, {"Content-Type": "application/json"});
        res.end(createResponse({error: "Unauthorized"}, 401));
        return;
    }

    // Handle different request types
    if (req.method === "GET" && req.url === "/status") {
        // GET /status - Server status
        let status = {
            status: "running",
            version: "6.5.5.10",
            uptime: Math.floor((Date.now() - server_state.start_time) / 1000),
            kernel_type: "accessibility",
            running: server_state.running,
            current_task: server_state.current_task,
            supported_kernels: ["accessibility", "coordinate"],
            features: {
                recording: false,
                ai_intervention: false,
                anti_detection: true,
                ocr: false
            }
        };
        res.writeHead(200, {"Content-Type": "application/json"});
        res.end(createResponse(status));

    } else if (req.method === "POST") {
        let body = "";

        req.on("data", chunk => body += chunk);
        req.on("end", () => {
            try {
                let data = body ? JSON.parse(body) : {};

                if (req.url === "/execute") {
                    // POST /execute - Execute task
                    handleExecute(data, res);
                } else if (req.url === "/check_status") {
                    // POST /check_status - Check status
                    handleCheckStatus(data, res);
                } else if (req.url === "/stop") {
                    // POST /stop - Stop task
                    handleStop(data, res);
                } else {
                    res.writeHead(404, {"Content-Type": "application/json"});
                    res.end(createResponse({error: "Not Found"}, 404));
                }

            } catch (e) {
                console.error("Error handling request:", e);
                res.writeHead(500, {"Content-Type": "application/json"});
                res.end(createResponse({error: e.message}, 500));
            }
        });
    } else {
        res.writeHead(405, {"Content-Type": "application/json"});
        res.end(createResponse({error: "Method Not Allowed"}, 405);
    }
});

function handleExecute(data, res) {
    console.log("Executing task:", data.id);

    // Set server state
    server_state.running = true;
    server_state.current_task = {
        id: data.id,
        workflow_id: data.metadata?.workflow_id,
        progress: 0,
        started_at: new Date().toISOString()
    };

    // Validate task
    if (!data.id || !data.steps || !Array.isArray(data.steps)) {
        res.writeHead(400, {"Content-Type": "application/json"});
        res.end(createResponse({
            success: false,
            error: "Invalid task structure"
        }, 400));
        return;
    }

    // Execute steps (simplified for MVP)
    let steps_result = [];
    let total_steps = data.steps.length;

    for (let i = 0; i < total_steps; i++) {
        let step = data.steps[i];
        let step_id = step.step_id || `step_${String(i+1).padStart(3, '0')}`;

        try {
            let step_result = executeStep(step, step_id);
            steps_result.push(step_result);

            // Update progress
            server_state.current_task.progress = (i + 1) / total_steps;

        } catch (e) {
            console.error("Step error:", e);
            steps_result.push({
                step_id: step_id,
                success: false,
                error: e.message
            });
            break;
        }
    }

    // Reset state
    server_state.running = false;
    server_state.current_task = null;

    let result = {
        task_id: data.id,
        status: "completed",
        steps_result: steps_result,
        total_duration_ms: 1000,
        completed_at: new Date().toISOString()
    };

    res.writeHead(200, {"Content-Type": "application/json"});
    res.end(createResponse({
        success: true,
        result: result
    }));
}

function handleCheckStatus(data, res) {
    let status = {
        running: server_state.running,
        current_task: server_state.current_task,
        progress: server_state.current_task?.progress || 0,
        uptime: Math.floor((Date.now() - server_state.start_time) / 1000),
        kernel_type: "accessibility",
        memory_usage: "45MB",
        cpu_usage: "12%"
    };

    res.writeHead(200, {"Content-Type": "application/json"});
    res.end(createResponse(status));
}

function handleStop(data, res) {
    if (server_state.current_task) {
        server_state.current_task.stopped = true;
        server_state.running = false;

        res.writeHead(200, {"Content-Type": "application/json"});
        res.end(createResponse({
            success: true,
            message: "Task stopped successfully",
            stopped_task_id: server_state.current_task.id
        }));
    } else {
        res.writeHead(400, {"Content-Type": "application/json"});
        res.end(createResponse({
            error: "No task running"
        }, 400));
    }
}

function executeStep(step, stepId) {
    let action = step.action;
    let startTime = Date.now();

    if (action === "click") {
        return executeClick(step, stepId, startTime);
    } else if (action === "input") {
        return executeInput(step, stepId, startTime);
    } else if (action === "swipe") {
        return executeSwipe(step, stepId, startTime);
    } else if (action === "wait") {
        return executeWait(step, stepId, startTime);
    } else {
        throw new Error("Unknown action: " + action);
    }
}

function executeClick(step, stepId, startTime) {
    // MVP: Simulate click execution
    return {
        step_id: stepId,
        success: true,
        duration_ms: Date.now() - startTime
    };
}

function executeInput(step, stepId, startTime) {
    // MVP: Simulate input execution
    return {
        step_id: stepId,
        success: true,
        duration_ms: Date.now() - startTime,
        value: step.value || ""
    };
}

function executeSwipe(step, stepId, startTime) {
    // MVP: Simulate swipe execution
    return {
        step_id: stepId,
        success: true,
        duration_ms: step.duration || 300
    };
}

function executeWait(step, stepId, startTime) {
    // MVP: Simulate wait
    let timeout = step.condition?.timeout || 5000;
    // Don't actually wait in MVP
    return {
        step_id: stepId,
        success: true,
        duration_ms: Math.min(timeout, 5000)
    };
}

// Start server
server.listen(8765);
toast("ClawMobile API Server started on port 8765");
console.log("API Server ready to accept requests");
'''

    return script


def get_membership_endpoints() -> Dict[str, Any]:
    """Get membership API endpoints"""
    return {
        "activate": {
            "path": "/api/v1/membership/redeem",
            "method": "POST",
            "description": "兑换码激活"
        },
        "status": {
            "path": "/api/v1/membership/status",
            "method": "GET",
            "description": "查询会员状态"
        },
        "validate": {
            "path": "/api/v1/membership/validate",
            "method": "POST",
            "description": "验证兑换码"
        }
    }
