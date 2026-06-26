"""
Hook Manager - Unified Hook framework for Anima AIOS
Supports pre_execute, post_execute, on_error triggers with priority ordering
"""
import asyncio
import time
import uuid
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional

from .hook_store import HookStore, HookTrigger, Priority, HookMetadata, HookExecution


class HookManager:
    """Hook Manager - Unified Hook framework"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize Hook Manager
        
        Args:
            config_dir: Configuration directory path (default: ~/.anima/config)
        """
        self.config_dir = Path(config_dir or "~/.anima/config").expanduser()
        self.hooks_dir = Path("~/.anima/hooks").expanduser()
        self.hooks_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Hook Store (SQLite)
        self.hook_store = HookStore(self.config_dir / "hooks.db")
        
        # In-memory registry
        self.registered_hooks: Dict[str, HookMetadata] = {}
        self.hook_functions: Dict[str, Callable] = {}
        
        # Load existing hooks from store
        self._load_hooks_from_store()
        
        # Register builtin hooks
        self._register_builtin_hooks()
    
    def _load_hooks_from_store(self) -> None:
        """Load hooks from persistent store"""
        hooks = self.hook_store.get_all_hooks()
        for hook_data in hooks:
            metadata = HookMetadata(
                name=hook_data["name"],
                description=hook_data["description"],
                trigger=HookTrigger(hook_data["trigger"]),
                priority=Priority(hook_data["priority"]),
                enabled=hook_data["enabled"],
                timeout_ms=hook_data["timeout_ms"],
                retry_count=hook_data["retry_count"]
            )
            self.registered_hooks[hook_data["name"]] = metadata
    
    def _register_builtin_hooks(self) -> None:
        """Register builtin hooks"""
        # Learning Logger Hook (post-execute only, no function yet)
        self.register_hook_metadata(
            name="learning_logger",
            description="自动记录学习行为到 .learnings/ 目录",
            trigger=HookTrigger.POST_EXECUTE,
            priority=Priority.HIGH
        )
        
        # Auth Check Hook (pre-execute only, no function yet)
        self.register_hook_metadata(
            name="auth_check",
            description="执行前权限检查",
            trigger=HookTrigger.PRE_EXECUTE,
            priority=Priority.CRITICAL
        )
        
        # Error Handler Hook (on-error only, no function yet)
        self.register_hook_metadata(
            name="error_handler",
            description="错误时自动记录和重试",
            trigger=HookTrigger.ON_ERROR,
            priority=Priority.CRITICAL
        )
    
    def register_hook_metadata(
        self,
        name: str,
        description: str,
        trigger: HookTrigger,
        priority: Priority = Priority.MEDIUM,
        enabled: bool = True,
        timeout_ms: int = 5000,
        retry_count: int = 0
    ) -> None:
        """Register hook metadata only (without function)"""
        if name in self.registered_hooks:
            # Update existing
            metadata = HookMetadata(
                name=name,
                description=description,
                trigger=trigger,
                priority=priority,
                enabled=enabled,
                timeout_ms=timeout_ms,
                retry_count=retry_count
            )
        else:
            # Create new
            metadata = HookMetadata(
                name=name,
                description=description,
                trigger=trigger,
                priority=priority,
                enabled=enabled,
                timeout_ms=timeout_ms,
                retry_count=retry_count
            )
        
        self.registered_hooks[name] = metadata
        self.hook_store.save_hook(name, metadata)
    
    def register_hook(
        self,
        name: str,
        description: str,
        trigger: HookTrigger,
        priority: Priority = Priority.MEDIUM,
        func: Optional[Callable] = None,
        enabled: bool = True,
        timeout_ms: int = 5000,
        retry_count: int = 0
    ) -> None:
        """
        Register a hook with metadata and optional function
        
        Args:
            name: Hook name (unique identifier)
            description: Hook description
            trigger: When the hook should be triggered
            priority: Hook execution priority
            func: Hook function to execute
            enabled: Whether hook is enabled
            timeout_ms: Execution timeout in milliseconds
            retry_count: Number of retries on failure
        """
        metadata = HookMetadata(
            name=name,
            description=description,
            trigger=trigger,
            priority=priority,
            enabled=enabled,
            timeout_ms=timeout_ms,
            retry_count=retry_count
        )
        
        self.registered_hooks[name] = metadata
        
        if func:
            self.hook_functions[name] = func
        
        # Persist to store
        self.hook_store.save_hook(name, metadata)
    
    def unregister_hook(self, name: str) -> bool:
        """
        Unregister a hook
        
        Args:
            name: Hook name to unregister
            
        Returns:
            True if hook was removed, False if not found
        """
        if name not in self.registered_hooks:
            return False
        
        del self.registered_hooks[name]
        
        if name in self.hook_functions:
            del self.hook_functions[name]
        
        self.hook_store.delete_hook(name)
        return True
    
    def enable_hook(self, name: str) -> bool:
        """
        Enable a hook
        
        Args:
            name: Hook name to enable
            
        Returns:
            True if hook was enabled, False if not found
        """
        if name not in self.registered_hooks:
            return False
        
        self.registered_hooks[name].enabled = True
        self.hook_store.update_hook_status(name, True)
        return True
    
    def disable_hook(self, name: str) -> bool:
        """
        Disable a hook
        
        Args:
            name: Hook name to disable
            
        Returns:
            True if hook was disabled, False if not found
        """
        if name not in self.registered_hooks:
            return False
        
        self.registered_hooks[name].enabled = False
        self.hook_store.update_hook_status(name, False)
        return True
    
    def get_hook(self, name: str) -> Optional[HookMetadata]:
        """Get hook metadata by name"""
        return self.registered_hooks.get(name)
    
    def get_hooks_by_trigger(self, trigger: HookTrigger) -> List[HookMetadata]:
        """Get all hooks for a specific trigger"""
        return [
            metadata
            for metadata in self.registered_hooks.values()
            if metadata.trigger == trigger and metadata.enabled
        ]
    
    def list_hooks(self) -> List[Dict]:
        """List all registered hooks with their status"""
        result = []
        for name, metadata in self.registered_hooks.items():
            stats = self.hook_store.get_hook_stats(name)
            result.append({
                "name": name,
                "description": metadata.description,
                "trigger": metadata.trigger.value,
                "priority": metadata.priority.name,
                "enabled": metadata.enabled,
                "has_function": name in self.hook_functions,
                "stats": stats
            })
        return result
    
    async def execute_pre_hooks(self, context: Dict[str, Any]) -> bool:
        """
        Execute all PRE_EXECUTE hooks
        
        Args:
            context: Execution context containing task_id, action, etc.
            
        Returns:
            True if all critical hooks succeeded, False otherwise
        """
        return await self._execute_hooks_by_trigger(
            HookTrigger.PRE_EXECUTE,
            context
        )
    
    async def execute_post_hooks(self, context: Dict[str, Any]) -> None:
        """
        Execute all POST_EXECUTE hooks
        
        Args:
            context: Execution context containing task_id, action, result, etc.
        """
        await self._execute_hooks_by_trigger(
            HookTrigger.POST_EXECUTE,
            context
        )
    
    async def execute_error_hooks(self, context: Dict[str, Any], error: Exception) -> None:
        """
        Execute all ON_ERROR hooks
        
        Args:
            context: Execution context
            error: The error that occurred
        """
        context["error"] = str(error)
        context["error_type"] = type(error).__name__
        
        await self._execute_hooks_by_trigger(
            HookTrigger.ON_ERROR,
            context
        )
    
    async def execute_success_hooks(self, context: Dict[str, Any]) -> None:
        """
        Execute all ON_SUCCESS hooks
        
        Args:
            context: Execution context
        """
        await self._execute_hooks_by_trigger(
            HookTrigger.ON_SUCCESS,
            context
        )
    
    async def _execute_hooks_by_trigger(
        self,
        trigger: HookTrigger,
        context: Dict[str, Any]
    ) -> bool:
        """
        Execute hooks by trigger type with priority ordering
        
        Args:
            trigger: The trigger type
            context: Execution context
            
        Returns:
            True if all critical hooks succeeded (for PRE_EXECUTE)
        """
        # Get hooks for this trigger
        hooks = [
            (name, metadata)
            for name, metadata in self.registered_hooks.items()
            if metadata.trigger == trigger and metadata.enabled
        ]
        
        # Sort by priority (lower number = higher priority)
        hooks.sort(key=lambda x: x[1].priority.value)
        
        if not hooks:
            return True
        
        success = True
        
        for name, metadata in hooks:
            execution = await self._execute_single_hook(name, metadata, context)
            
            if execution.status == "failed":
                if metadata.priority == Priority.CRITICAL:
                    success = False
        
        return success
    
    async def _execute_single_hook(
        self,
        name: str,
        metadata: HookMetadata,
        context: Dict[str, Any]
    ) -> HookExecution:
        """
        Execute a single hook with timing and error handling
        
        Args:
            name: Hook name
            metadata: Hook metadata
            context: Execution context
            
        Returns:
            HookExecution record
        """
        func = self.hook_functions.get(name)
        
        # If no function registered, skip
        if not func:
            return HookExecution(
                hook_id=name,
                task_id=context.get("task_id", "unknown"),
                status="skipped",
                duration_ms=0.0,
                error="No function registered"
            )
        
        start_time = time.time()
        
        try:
            # Execute with timeout
            if asyncio.iscoroutinefunction(func):
                result = await asyncio.wait_for(
                    func(context),
                    timeout=metadata.timeout_ms / 1000.0
                )
            else:
                result = func(context)
            
            duration_ms = (time.time() - start_time) * 1000
            
            execution = HookExecution(
                hook_id=name,
                task_id=context.get("task_id", "unknown"),
                status="success",
                duration_ms=duration_ms
            )
        
        except asyncio.TimeoutError:
            duration_ms = (time.time() - start_time) * 1000
            
            execution = HookExecution(
                hook_id=name,
                task_id=context.get("task_id", "unknown"),
                status="failed",
                duration_ms=duration_ms,
                error=f"Timeout after {metadata.timeout_ms}ms"
            )
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            execution = HookExecution(
                hook_id=name,
                task_id=context.get("task_id", "unknown"),
                status="failed",
                duration_ms=duration_ms,
                error=f"{type(e).__name__}: {str(e)}"
            )
        
        # Save execution record
        self.hook_store.save_execution(execution)
        
        return execution
    
    def get_hook_stats(self, name: str) -> Dict:
        """Get execution statistics for a hook"""
        if name not in self.registered_hooks:
            return {}
        return self.hook_store.get_hook_stats(name)
    
    def get_hook_executions(self, name: str, limit: int = 10) -> List[Dict]:
        """Get recent executions for a hook"""
        return self.hook_store.get_recent_executions(name, limit)
    
    def register_function(self, name: str, func: Callable) -> bool:
        """
        Register a function for an existing hook
        
        Args:
            name: Hook name
            func: Function to register
            
        Returns:
            True if function was registered, False if hook not found
        """
        if name not in self.registered_hooks:
            return False
        
        self.hook_functions[name] = func
        return True
    
    def clear_all_hooks(self) -> int:
        """
        Clear all hooks (for testing)
        
        Returns:
            Number of hooks cleared
        """
        count = len(self.registered_hooks)
        
        for name in list(self.registered_hooks.keys()):
            self.unregister_hook(name)
        
        return count
