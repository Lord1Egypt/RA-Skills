"""Base class for PDE problems."""

from abc import ABC, abstractmethod
import tensorflow as tf


class BaseProblem(ABC):
    """Base class for PDE problems."""
    
    # 默认配置 - 从 config 中读取，不再作为类属性
    # 这些将在 __init__ 中从 config 加载
    
    def __init__(self, config):
        """
        Initialize problem with configuration.
        Automatically extracts parameters and handles multi-dimensional bounds.
        
        Args:
            config: Configuration object with problem parameters
        """
        import numpy as np
        
        self.config = config
        self.d = config.dimension
        self.T = config.T
        self.t_low = config.t_low
        
        # 自动处理多维边界
        # X_low 和 X_high 可以是标量（1D）或列表（多维）
        if isinstance(config.X_low, (list, tuple)):
            self.X_low = np.array(config.X_low)
        else:
            # 标量情况：如果dimension > 1，复制到所有维度；否则保持标量
            if self.d > 1:
                self.X_low = np.full(self.d, config.X_low)
            else:
                self.X_low = config.X_low
        
        if isinstance(config.X_high, (list, tuple)):
            self.X_high = np.array(config.X_high)
        else:
            if self.d > 1:
                self.X_high = np.full(self.d, config.X_high)
            else:
                self.X_high = config.X_high
        
        # 从 config 加载问题配置
        self.num_controls = config.num_controls
        self.control_names = config.control_names or [f'u{i}' for i in range(self.num_controls)]
        self.metrics_config = config.metrics_config or ['maxdiff_V', 'maxdiff_terminal']
        self.extra_info_mapping = config.extra_info_mapping or {}
        self.early_stop_metric = config.early_stop_metric
        self.early_stop_threshold = config.early_stop_threshold
        self.problem_params_keys = config.problem_params_keys or []
        self.custom_metrics = config.custom_metrics or {}
        
        # 自动从config提取problem_params_keys中列出的参数
        for key in self.problem_params_keys:
            if key in ('T', 'd', 'dimension'):  # 已经手动设置了
                continue
            if hasattr(config, key):
                setattr(self, key, getattr(config, key))
    
    def get_domain_bounds(self):
        """
        Get the domain bounds for the problem.
        Default implementation uses standard bounds from config.
        Override if you need custom bounds.
        
        Returns:
            Dictionary with t_low, t_high, X_low, X_high
        """
        return {
            't_low': self.t_low,
            't_high': self.T,
            'X_low': self.X_low,
            'X_high': self.X_high
        }
    
    def analytical_solution(self, t, x):
        """
        Compute analytical solution if available.
        Default: returns None (no analytical solution).
        Override this method if analytical solution exists.
        
        Args:
            t: Time points
            x: Space points
            
        Returns:
            Analytical solution values or None
        """
        return None
    
    def get_num_controls(self):
        """Get number of control variables (uses class attribute)."""
        return self.num_controls
    
    def get_control_names(self):
        """Get names of control variables (uses class attribute)."""
        return self.control_names
    
    def get_metrics_config(self):
        """Get metrics to track during training (uses class attribute)."""
        return self.metrics_config
    
    def extract_metrics(self, validation_results, t_eval, X_eval, model, control):
        """
        Extract problem-specific metrics from validation results.
        Uses extra_info_mapping to automatically extract metrics from extra_info dict.
        Override this method only if you need custom metric computation.
        
        Args:
            validation_results: Tuple (L1_val, L3_val, diff_V_val, diff_terminal_val, L2_val, extra_info)
            t_eval: Evaluation time point
            X_eval: Evaluation space point
            model: Value function model
            control: Control model
            
        Returns:
            Dictionary of {metric_name: value}
        """
        import numpy as np
        
        (L1_val, L3_val, diff_V_val, diff_terminal_val,
         L2_val, extra_info) = validation_results
        
        # Compute basic metrics.
        # diff_V_val may be a plain tensor or a dict of debug tensors (e.g.
        # {'residual': ..., 'V': ..., 'V_t': ..., 'V_x': ...}).
        # When it is a dict, use the 'residual' key; fall back to the first value.
        if isinstance(diff_V_val, dict):
            _diff_V_tensor = diff_V_val.get('residual', next(iter(diff_V_val.values())))
        else:
            _diff_V_tensor = diff_V_val
        metrics = {
            'maxdiff_V': float(np.max(np.abs(_diff_V_tensor.numpy()))),
            'maxdiff_terminal': float(np.max(np.abs(diff_terminal_val.numpy()))),
        }
        
        # Extract metrics from extra_info using mapping
        for extra_key, metric_name in self.extra_info_mapping.items():
            if extra_key in extra_info:
                val = extra_info[extra_key]
                if hasattr(val, 'numpy'):
                    metrics[metric_name] = float(np.max(np.abs(val.numpy())))
                else:
                    metrics[metric_name] = float(val)
        
        # Evaluate at origin
        V_pred = model(t_eval, X_eval)
        out_pred = control(t_eval, X_eval)
        
        metrics['V_at_origin'] = float(V_pred.numpy()[0, 0])
        
        # Add all control values
        for idx, control_name in enumerate(self.get_control_names()):
            metrics[control_name] = float(out_pred[0, idx].numpy())
        
        # 自动计算自定义指标
        for metric_name, (operation, operands) in self.custom_metrics.items():
            try:
                values = [metrics[op] for op in operands]
                if operation == 'add':
                    metrics[metric_name] = sum(values)
                elif operation == 'subtract':
                    metrics[metric_name] = values[0] - sum(values[1:])
                elif operation == 'multiply':
                    result = 1
                    for v in values:
                        result *= v
                    metrics[metric_name] = result
                elif operation == 'divide':
                    metrics[metric_name] = values[0] / values[1] if len(values) == 2 else None
            except (KeyError, ZeroDivisionError):
                pass  # 如果操作数不存在或除零，忽略
        
        return metrics
    
    def format_stage_info(self, stage, metrics, losses):
        """
        Format stage information for printing.
        根据 config.print_metrics 自动格式化输出。
        如果需要完全自定义格式，可以 override。
        
        Args:
            stage: Current training stage
            metrics: Dictionary of metrics from extract_metrics
            losses: Dictionary with L1, L2, L3
            
        Returns:
            String to print
        """
        lines = [f"\nStage {stage}:"]
        
        # 获取要打印的指标列表
        print_list = self.config.print_metrics if hasattr(self.config, 'print_metrics') and self.config.print_metrics else None
        
        # 合并所有可用的数据
        all_data = {**losses, **metrics}
        
        if print_list is None:
            # 打印所有指标（按类别分组）
            # 1. 主要指标
            main_metrics = ['maxdiff_V', 'maxdiff_terminal']
            main_parts = [f"{k}={all_data[k]:.4e}" for k in main_metrics if k in all_data]
            if main_parts:
                lines.append(f"  {', '.join(main_parts)}")
            
            # 2. 其他验证指标
            other_metrics = [k for k in metrics.keys() if k not in main_metrics + ['V_at_origin'] + self.control_names]
            if other_metrics:
                other_parts = [f"{k}={all_data[k]:.4e}" for k in other_metrics]
                lines.append(f"  {', '.join(other_parts)}")
            
            # 3. Losses
            loss_parts = [f"{k}={losses[k]:.4e}" for k in ['L1', 'L2', 'L3'] if k in losses]
            if loss_parts:
                lines.append(f"  {', '.join(loss_parts)}")
            
            # 4. V at origin
            if 'V_at_origin' in all_data:
                lines.append(f"  V(0,...)={all_data['V_at_origin']:.6f}")
            
            # 5. 控制变量
            control_parts = [f"{k}(0,...)={all_data[k]:.6f}" for k in self.control_names if k in all_data]
            if control_parts:
                lines.append(f"  {', '.join(control_parts)}")
        else:
            # 按照用户指定的列表打印
            for key in print_list:
                if key in all_data:
                    val = all_data[key]
                    # 根据数值大小选择格式
                    if abs(val) < 1e-2 or abs(val) > 1e3:
                        lines.append(f"  {key}={val:.4e}")
                    else:
                        lines.append(f"  {key}={val:.6f}")
        
        return '\n'.join(lines)
    
    def check_early_stopping(self, metrics, stage):
        """
        Check if training should stop early.
        Uses early_stop_metric and early_stop_threshold class attributes.
        
        Args:
            metrics: Dictionary of current metrics
            stage: Current training stage
            
        Returns:
            bool: True if training should stop, False otherwise
        """
        if self.early_stop_metric in metrics:
            return metrics[self.early_stop_metric] < self.early_stop_threshold
        return False
    
    @abstractmethod
    def get_terminal_condition(self, x):
        """
        Get terminal condition for the problem.
        
        REQUIRED: Must implement this method for your problem.
        
        Args:
            x: Space points (TensorFlow tensor)
            
        Returns:
            Terminal condition values (TensorFlow tensor)
            
        Example:
            def get_terminal_condition(self, x):
                import tensorflow as tf
                return tf.square(x)  # g(x) = x^2
        """
        pass
    
    def get_problem_params(self):
        """
        Get problem-specific parameters for saving/logging.
        Automatically collects parameters listed in problem_params_keys.
        
        Returns:
            Dictionary of problem parameters
        """
        params = {}
        for key in self.problem_params_keys:
            if hasattr(self, key):
                val = getattr(self, key)
                # Convert numpy arrays to lists for JSON serialization
                if hasattr(val, 'tolist'):
                    val = val.tolist()
                params[key] = val
        return params
    
    def get_control_constraints(self):
        """
        Get control constraints for the problem.
        默认实现：自动收集以 'C' 开头的约束参数。
        Override 如果需要自定义逻辑。
        
        Returns:
            Dictionary with constraint parameters
        """
        constraints = {}
        # 自动收集以 'C' 开头的约束参数（如 Cbeta_up, CbetaZ_up）
        for key in self.problem_params_keys:
            if key.startswith('C') and hasattr(self, key):
                constraints[key] = getattr(self, key)
        # 添加 case 参数（如果存在）
        if hasattr(self, 'case'):
            constraints['case'] = self.case
        return constraints
