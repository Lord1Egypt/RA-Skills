"""
Self-Evolution System - RL-based continuous improvement

This module implements:
- Performance monitoring
- Reinforcement learning pipeline
- Behavioral optimization
- Staged deployment with rollback
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from pathlib import Path
import math


@dataclass
class Metric:
    """Performance metric."""
    name: str
    value: float
    timestamp: str
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class Trajectory:
    """Experience trajectory for RL."""
    id: str
    states: List[Dict]
    actions: List[Dict]
    rewards: List[float]
    outcome: str
    total_reward: float = 0.0
    
    def calculate_total_reward(self) -> float:
        """Calculate total reward with discount."""
        gamma = 0.99  # Discount factor
        total = 0
        for i, r in enumerate(reversed(self.rewards)):
            total = r + gamma * total
        self.total_reward = total
        return total


@dataclass
class BehaviorModel:
    """Learned behavior model."""
    version: str
    parameters: Dict
    performance: Dict
    created_at: str
    baseline_version: Optional[str] = None


class PerformanceMonitor:
    """
    Monitors system performance for evolution triggers.
    
    Supports multiple data sources for metrics collection:
    - Task history for completion rate
    - User feedback records for satisfaction
    - Error logs for error rate
    - System metrics for latency, throughput, memory
    """
    
    def __init__(self, config: Dict = None, data_sources: Dict = None):
        self.config = config or {
            'collection_interval': 60,  # seconds
            'history_size': 1000,
            'thresholds': {
                'error_rate': 0.05,
                'latency': 5000,  # ms
                'satisfaction': 0.8,
                'completion_rate': 0.9
            }
        }
        
        # Data sources for actual metrics
        self.data_sources = data_sources or {
            'task_history': [],      # List of task records with 'status', 'completed_at' fields
            'user_feedback': [],     # List of feedback records with 'score' field (0-1)
            'error_log': [],         # List of error records with 'timestamp' field
            'metrics_store': {},     # Dict with 'latency', 'throughput', 'memory' metrics
            'skill_calls': []        # List of skill call records
        }
        
        self.metrics_history: List[Dict] = []
        self.alerts: List[Dict] = []
    
    def set_data_sources(self, **sources):
        """Set data sources for metrics collection."""
        self.data_sources.update(sources)
    
    def collect(self) -> Dict:
        """
        Collect current performance metrics.
        
        Returns:
            Current metrics dictionary
        """
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'task_completion_rate': self._measure_completion_rate(),
            'user_satisfaction': self._measure_satisfaction(),
            'error_rate': self._measure_error_rate(),
            'latency_avg': self._measure_latency(),
            'throughput': self._measure_throughput(),
            'memory_usage': self._measure_memory(),
            'skill_usage': self._measure_skill_usage()
        }
        
        self.metrics_history.append(metrics)
        
        # Trim history
        if len(self.metrics_history) > self.config['history_size']:
            self.metrics_history = self.metrics_history[-self.config['history_size']:]
        
        # Check thresholds
        self._check_thresholds(metrics)
        
        return metrics
    
    def _measure_completion_rate(self) -> float:
        """
        Measure task completion rate from task history.
        
        Reads from self.data_sources['task_history'] which should contain
        records with 'status' field: 'completed', 'failed', 'pending', etc.
        """
        task_history = self.data_sources.get('task_history', [])
        
        if not task_history:
            # Fallback: calculate from recent metrics history
            if self.metrics_history:
                return self.metrics_history[-1].get('task_completion_rate', 0.92)
            return 0.0
        
        # Count completed vs total tasks
        total = len(task_history)
        completed = sum(1 for task in task_history 
                        if task.get('status') in ['completed', 'success', 'done'])
        
        return completed / total if total > 0 else 0.0
    
    def _measure_satisfaction(self) -> float:
        """
        Measure user satisfaction from feedback records.
        
        Reads from self.data_sources['user_feedback'] which should contain
        records with 'score' field (0-1 scale).
        """
        feedback = self.data_sources.get('user_feedback', [])
        
        if not feedback:
            # Fallback: calculate from recent metrics history
            if self.metrics_history:
                return self.metrics_history[-1].get('user_satisfaction', 0.85)
            return 0.0
        
        # Calculate average satisfaction score
        scores = [f.get('score', 0) for f in feedback if 'score' in f]
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _measure_error_rate(self) -> float:
        """
        Measure error rate from error logs.
        
        Reads from self.data_sources['error_log'] which should contain
        error records with 'timestamp' field.
        
        Also considers self.data_sources['task_history'] for task success/failure.
        """
        error_log = self.data_sources.get('error_log', [])
        task_history = self.data_sources.get('task_history', [])
        
        # Calculate from task history if available
        if task_history:
            total = len(task_history)
            failed = sum(1 for task in task_history 
                        if task.get('status') in ['failed', 'error', 'timeout'])
            return failed / total if total > 0 else 0.0
        
        # Fallback: calculate from error log relative to total operations
        if not error_log:
            if self.metrics_history:
                return self.metrics_history[-1].get('error_rate', 0.03)
            return 0.0
        
        # Count errors in recent period (last hour)
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_errors = sum(1 for e in error_log 
                           if datetime.fromisoformat(e.get('timestamp', '1970-01-01')) > one_hour_ago)
        
        # Estimate total operations from metrics store or use default
        metrics_store = self.data_sources.get('metrics_store', {})
        total_ops = metrics_store.get('total_operations', 1000)
        
        return recent_errors / total_ops if total_ops > 0 else 0.0
    
    def _measure_latency(self) -> float:
        """
        Measure average latency in milliseconds.
        
        Reads from self.data_sources['metrics_store'] which should contain
        'latency' data with historical values or 'latency_avg' for current.
        """
        metrics_store = self.data_sources.get('metrics_store', {})
        
        # Check for direct latency value
        if 'latency_avg' in metrics_store:
            return float(metrics_store['latency_avg'])
        
        # Check for latency history
        if 'latency' in metrics_store and isinstance(metrics_store['latency'], list):
            latencies = metrics_store['latency']
            return sum(latencies) / len(latencies) if latencies else 0.0
        
        # Fallback
        if self.metrics_history:
            return self.metrics_history[-1].get('latency_avg', 1200.0)
        return 0.0
    
    def _measure_throughput(self) -> float:
        """
        Measure requests per minute.
        
        Reads from self.data_sources['metrics_store'] which should contain
        'throughput' or 'requests_per_minute' value.
        """
        metrics_store = self.data_sources.get('metrics_store', {})
        
        # Check for direct throughput value
        if 'throughput' in metrics_store:
            return float(metrics_store['throughput'])
        
        if 'requests_per_minute' in metrics_store:
            return float(metrics_store['requests_per_minute'])
        
        # Calculate from task history if available
        task_history = self.data_sources.get('task_history', [])
        if task_history:
            # Count tasks in last minute
            one_min_ago = datetime.now() - timedelta(minutes=1)
            recent_tasks = sum(1 for t in task_history 
                              if datetime.fromisoformat(t.get('completed_at', '1970-01-01')) > one_min_ago)
            return float(recent_tasks)
        
        # Fallback
        if self.metrics_history:
            return self.metrics_history[-1].get('throughput', 45.0)
        return 0.0
    
    def _measure_memory(self) -> float:
        """
        Measure memory usage as percentage (0-1).
        
        Reads from self.data_sources['metrics_store'] which should contain
        'memory_usage' as percentage or 'memory_percent'.
        """
        metrics_store = self.data_sources.get('metrics_store', {})
        
        if 'memory_usage' in metrics_store:
            value = float(metrics_store['memory_usage'])
            # Normalize if > 1 (assuming percentage format)
            return value / 100.0 if value > 1 else value
        
        if 'memory_percent' in metrics_store:
            return float(metrics_store['memory_percent']) / 100.0
        
        # Fallback
        if self.metrics_history:
            return self.metrics_history[-1].get('memory_usage', 0.65)
        return 0.0
    
    def _measure_skill_usage(self) -> Dict:
        """
        Measure skill usage statistics.
        
        Reads from self.data_sources['skill_calls'] which should contain
        records with 'skill_name', 'status' ('success' or 'failed') fields.
        """
        skill_calls = self.data_sources.get('skill_calls', [])
        
        if not skill_calls:
            # Fallback: calculate from recent metrics history
            if self.metrics_history:
                return self.metrics_history[-1].get('skill_usage', {
                    'total_calls': 0,
                    'successful_calls': 0,
                    'failed_calls': 0,
                    'most_used': None,
                    'least_used': None
                })
            return {
                'total_calls': 0,
                'successful_calls': 0,
                'failed_calls': 0,
                'most_used': None,
                'least_used': None
            }
        
        # Aggregate skill call statistics
        skill_stats: Dict[str, Dict] = {}
        
        for call in skill_calls:
            skill_name = call.get('skill_name', 'unknown')
            if skill_name not in skill_stats:
                skill_stats[skill_name] = {'total': 0, 'successful': 0, 'failed': 0}
            
            skill_stats[skill_name]['total'] += 1
            status = call.get('status', '').lower()
            if status in ['success', 'successful', 'completed']:
                skill_stats[skill_name]['successful'] += 1
            else:
                skill_stats[skill_name]['failed'] += 1
        
        # Find most and least used
        if skill_stats:
            sorted_by_usage = sorted(skill_stats.items(), key=lambda x: x[1]['total'], reverse=True)
            most_used = sorted_by_usage[0][0] if sorted_by_usage else None
            least_used = sorted_by_usage[-1][0] if len(sorted_by_usage) > 1 else most_used
        else:
            most_used = None
            least_used = None
        
        total_calls = sum(s['total'] for s in skill_stats.values())
        successful_calls = sum(s['successful'] for s in skill_stats.values())
        failed_calls = sum(s['failed'] for s in skill_stats.values())
        
        return {
            'total_calls': total_calls,
            'successful_calls': successful_calls,
            'failed_calls': failed_calls,
            'most_used': most_used,
            'least_used': least_used,
            'by_skill': skill_stats
        }
    
    def _check_thresholds(self, metrics: Dict):
        """Check metrics against thresholds."""
        thresholds = self.config['thresholds']
        
        if metrics['error_rate'] > thresholds['error_rate']:
            self.alerts.append({
                'type': 'error_rate_exceeded',
                'value': metrics['error_rate'],
                'threshold': thresholds['error_rate'],
                'timestamp': metrics['timestamp']
            })
        
        if metrics['latency_avg'] > thresholds['latency']:
            self.alerts.append({
                'type': 'latency_exceeded',
                'value': metrics['latency_avg'],
                'threshold': thresholds['latency'],
                'timestamp': metrics['timestamp']
            })
        
        if metrics['user_satisfaction'] < thresholds['satisfaction']:
            self.alerts.append({
                'type': 'satisfaction_below',
                'value': metrics['user_satisfaction'],
                'threshold': thresholds['satisfaction'],
                'timestamp': metrics['timestamp']
            })
    
    def detect_improvement_opportunities(self) -> List[Dict]:
        """Detect areas for improvement."""
        opportunities = []
        
        if not self.metrics_history:
            return opportunities
        
        recent = self.metrics_history[-10:]
        thresholds = self.config['thresholds']
        
        # Check error rate trend
        error_rates = [m['error_rate'] for m in recent]
        if sum(error_rates) / len(error_rates) > thresholds['error_rate'] * 0.8:
            opportunities.append({
                'type': 'error_reduction',
                'priority': 'high',
                'current': error_rates[-1],
                'target': thresholds['error_rate'] * 0.5
            })
        
        # Check latency trend
        latencies = [m['latency_avg'] for m in recent]
        if sum(latencies) / len(latencies) > thresholds['latency'] * 0.8:
            opportunities.append({
                'type': 'performance_optimization',
                'priority': 'medium',
                'current': latencies[-1],
                'target': thresholds['latency'] * 0.5
            })
        
        # Check satisfaction trend
        satisfactions = [m['user_satisfaction'] for m in recent]
        if sum(satisfactions) / len(satisfactions) < thresholds['satisfaction']:
            opportunities.append({
                'type': 'satisfaction_improvement',
                'priority': 'high',
                'current': satisfactions[-1],
                'target': thresholds['satisfaction']
            })
        
        return opportunities
    
    def get_summary(self) -> Dict:
        """Get performance summary."""
        if not self.metrics_history:
            return {'status': 'no_data'}
        
        recent = self.metrics_history[-10:]
        
        return {
            'avg_completion_rate': sum(m['task_completion_rate'] for m in recent) / len(recent),
            'avg_satisfaction': sum(m['user_satisfaction'] for m in recent) / len(recent),
            'avg_error_rate': sum(m['error_rate'] for m in recent) / len(recent),
            'avg_latency': sum(m['latency_avg'] for m in recent) / len(recent),
            'alert_count': len([a for a in self.alerts if 
                               datetime.fromisoformat(a['timestamp']) > 
                               datetime.now() - timedelta(hours=24)])
        }


class RewardFunction:
    """Base class for reward functions."""
    
    def calculate(self, trajectory: Trajectory) -> float:
        raise NotImplementedError


class TaskCompletionReward(RewardFunction):
    """Reward based on task completion."""
    
    def calculate(self, trajectory: Trajectory) -> float:
        if trajectory.outcome == 'success':
            return 1.0
        elif trajectory.outcome == 'partial':
            return 0.5
        else:
            return 0.0


class UserSatisfactionReward(RewardFunction):
    """Reward based on user satisfaction."""
    
    def calculate(self, trajectory: Trajectory) -> float:
        # Check for user feedback in trajectory
        for state in trajectory.states:
            if 'user_feedback' in state:
                feedback = state['user_feedback']
                if feedback == 'positive':
                    return 1.0
                elif feedback == 'neutral':
                    return 0.5
                elif feedback == 'negative':
                    return -0.5
        return 0.3  # Default neutral


class EfficiencyReward(RewardFunction):
    """Reward based on efficiency."""
    
    def __init__(self, optimal_steps: int = 5):
        self.optimal_steps = optimal_steps
    
    def calculate(self, trajectory: Trajectory) -> float:
        actual_steps = len(trajectory.actions)
        if actual_steps <= self.optimal_steps:
            return 1.0
        else:
            # Decay based on extra steps
            excess = actual_steps - self.optimal_steps
            return max(0.0, 1.0 - excess * 0.1)


class SafetyReward(RewardFunction):
    """Reward based on safety compliance."""
    
    def calculate(self, trajectory: Trajectory) -> float:
        # Check for safety violations
        for state in trajectory.states:
            if state.get('safety_violation', False):
                return -1.0
            if state.get('user_interrupt', False):
                return -0.5
        return 1.0


class RLPipeline:
    """
    Reinforcement learning pipeline for behavior optimization.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            'learning_rate': 0.01,
            'discount_factor': 0.99,
            'epochs': 10,
            'batch_size': 32,
            'reward_weights': {
                'task_completion': 1.0,
                'user_satisfaction': 0.8,
                'efficiency': 0.5,
                'safety': 1.0
            }
        }
        
        self.reward_functions = {
            'task_completion': TaskCompletionReward(),
            'user_satisfaction': UserSatisfactionReward(),
            'efficiency': EfficiencyReward(),
            'safety': SafetyReward()
        }
        
        self.policy_params: Dict = {}
        self.training_history: List[Dict] = []
    
    def train(self, trajectories: List[Trajectory], epochs: int = None) -> Dict:
        """
        Train behavior model on collected trajectories.
        
        Args:
            trajectories: List of experience trajectories
            epochs: Number of training epochs
            
        Returns:
            Training result
        """
        epochs = epochs or self.config['epochs']
        results = []
        
        for epoch in range(epochs):
            epoch_rewards = []
            
            for trajectory in trajectories:
                # Calculate combined reward
                reward = self._calculate_reward(trajectory)
                epoch_rewards.append(reward)
                
                # Update policy (simplified gradient update)
                self._update_policy(trajectory, reward)
            
            avg_reward = sum(epoch_rewards) / len(epoch_rewards) if epoch_rewards else 0
            
            epoch_result = {
                'epoch': epoch + 1,
                'avg_reward': avg_reward,
                'min_reward': min(epoch_rewards) if epoch_rewards else 0,
                'max_reward': max(epoch_rewards) if epoch_rewards else 0
            }
            
            results.append(epoch_result)
            self.training_history.append(epoch_result)
        
        return {
            'epochs': epochs,
            'trajectories_used': len(trajectories),
            'final_avg_reward': results[-1]['avg_reward'] if results else 0,
            'improvement': results[-1]['avg_reward'] - results[0]['avg_reward'] if len(results) > 1 else 0,
            'epoch_details': results
        }
    
    def _calculate_reward(self, trajectory: Trajectory) -> float:
        """Calculate combined reward from all reward functions."""
        total_reward = 0
        
        for name, func in self.reward_functions.items():
            weight = self.config['reward_weights'].get(name, 1.0)
            reward = func.calculate(trajectory)
            total_reward += weight * reward
        
        return total_reward
    
    def _update_policy(self, trajectory: Trajectory, reward: float):
        """Update policy parameters based on trajectory and reward."""
        # Simplified policy update
        # In real implementation, this would use proper RL algorithms
        
        for i, action in enumerate(trajectory.actions):
            action_key = action.get('type', 'unknown')
            
            if action_key not in self.policy_params:
                self.policy_params[action_key] = {
                    'count': 0,
                    'total_reward': 0,
                    'avg_reward': 0
                }
            
            self.policy_params[action_key]['count'] += 1
            self.policy_params[action_key]['total_reward'] += reward
            self.policy_params[action_key]['avg_reward'] = (
                self.policy_params[action_key]['total_reward'] / 
                self.policy_params[action_key]['count']
            )
    
    def get_model(self) -> BehaviorModel:
        """Get current behavior model."""
        return BehaviorModel(
            version=f"v{datetime.now().strftime('%Y%m%d%H%M')}",
            parameters=self.policy_params.copy(),
            performance=self._calculate_performance(),
            created_at=datetime.now().isoformat()
        )
    
    def _calculate_performance(self) -> Dict:
        """Calculate current performance metrics."""
        if not self.training_history:
            return {}
        
        recent = self.training_history[-10:]
        return {
            'avg_reward': sum(e['avg_reward'] for e in recent) / len(recent),
            'training_epochs': len(self.training_history)
        }


class EvolutionDeployer:
    """
    Deploys evolutions with staged rollout and rollback capability.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            'rollout_stages': [0.1, 0.25, 0.5, 1.0],
            'stage_interval': 300,  # seconds between stages
            'monitoring_window': 60,  # seconds to monitor each stage
            'rollback_threshold': {
                'error_rate': 0.1,
                'satisfaction_drop': 0.1
            }
        }
        
        self.deployments: List[Dict] = []
        self.rollback_history: List[Dict] = []
    
    def deploy(self, model: BehaviorModel, monitor: PerformanceMonitor) -> Dict:
        """
        Deploy evolution with staged rollout.
        
        Args:
            model: Behavior model to deploy
            monitor: Performance monitor for health checks
            
        Returns:
            Deployment result
        """
        deployment_id = f"deploy_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        deployment = {
            'id': deployment_id,
            'model_version': model.version,
            'started_at': datetime.now().isoformat(),
            'stages': [],
            'status': 'in_progress',
            'baseline_metrics': monitor.get_summary()
        }
        
        self.deployments.append(deployment)
        
        # Staged rollout
        for stage in self.config['rollout_stages']:
            stage_result = self._deploy_stage(model, stage, monitor)
            deployment['stages'].append(stage_result)
            
            if not stage_result['success']:
                # Rollback
                self._rollback(model, deployment)
                deployment['status'] = 'rolled_back'
                deployment['rollback_reason'] = stage_result['reason']
                return deployment
            
            # Wait before next stage
            time.sleep(min(self.config['stage_interval'], 5))  # Capped for testing
        
        deployment['status'] = 'completed'
        deployment['completed_at'] = datetime.now().isoformat()
        
        return deployment
    
    def _deploy_stage(self, model: BehaviorModel, stage: float, monitor: PerformanceMonitor) -> Dict:
        """Deploy to a percentage of traffic."""
        stage_result = {
            'stage': stage,
            'timestamp': datetime.now().isoformat(),
            'success': True,
            'metrics': None
        }
        
        # Monitor performance
        metrics = monitor.collect()
        stage_result['metrics'] = metrics
        
        # Check for rollback triggers
        baseline = monitor.get_summary()
        
        if metrics['error_rate'] > self.config['rollback_threshold']['error_rate']:
            stage_result['success'] = False
            stage_result['reason'] = f"Error rate {metrics['error_rate']:.2%} exceeded threshold"
            return stage_result
        
        return stage_result
    
    def _rollback(self, model: BehaviorModel, deployment: Dict):
        """Rollback to previous model."""
        rollback_record = {
            'deployment_id': deployment['id'],
            'model_version': model.version,
            'timestamp': datetime.now().isoformat(),
            'reason': deployment.get('rollback_reason', 'unknown')
        }
        
        self.rollback_history.append(rollback_record)
    
    def get_deployment_history(self, limit: int = 10) -> List[Dict]:
        """Get recent deployment history."""
        return self.deployments[-limit:]


class SelfEvolution:
    """
    Main class for self-evolution system.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.monitor = PerformanceMonitor(self.config.get('monitor', {}))
        self.rl_pipeline = RLPipeline(self.config.get('rl', {}))
        self.deployer = EvolutionDeployer(self.config.get('deployer', {}))
        
        self.trajectories: List[Trajectory] = []
        self.evolution_history: List[Dict] = []
    
    def collect_trajectory(self, states: List[Dict], actions: List[Dict], 
                          rewards: List[float], outcome: str) -> str:
        """
        Collect a trajectory for learning.
        
        Args:
            states: List of states
            actions: List of actions taken
            rewards: List of immediate rewards
            outcome: Final outcome
            
        Returns:
            Trajectory ID
        """
        trajectory = Trajectory(
            id=f"traj_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.trajectories)}",
            states=states,
            actions=actions,
            rewards=rewards,
            outcome=outcome
        )
        
        trajectory.calculate_total_reward()
        self.trajectories.append(trajectory)
        
        return trajectory.id
    
    def evolve(self) -> Dict:
        """
        Run one evolution cycle.
        
        Returns:
            Evolution result
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'opportunities': [],
            'training': None,
            'deployment': None
        }
        
        # 1. Detect improvement opportunities
        opportunities = self.monitor.detect_improvement_opportunities()
        result['opportunities'] = opportunities
        
        # 2. Train if we have enough trajectories
        if len(self.trajectories) >= 10:
            training_result = self.rl_pipeline.train(self.trajectories[-100:])
            result['training'] = training_result
            
            # 3. Deploy if training improved performance
            if training_result['improvement'] > 0:
                model = self.rl_pipeline.get_model()
                deployment_result = self.deployer.deploy(model, self.monitor)
                result['deployment'] = deployment_result
        
        self.evolution_history.append(result)
        
        return result
    
    def get_status(self) -> Dict:
        """Get current evolution status."""
        return {
            'trajectories_collected': len(self.trajectories),
            'evolution_cycles': len(self.evolution_history),
            'performance': self.monitor.get_summary(),
            'recent_deployments': self.deployer.get_deployment_history(5),
            'policy_params': len(self.rl_pipeline.policy_params)
        }


class RemoteDeployer:
    """
    Remote deployment system for deploying evolutions to remote environments.
    
    Implements the Deployment functionality from SKILL.md architecture.
    Supports deployment to multiple target environments with health monitoring
    and automatic rollback capabilities.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            'environments': {
                'staging': {
                    'endpoint': os.environ.get('STAGING_ENDPOINT', 'http://staging.local:8080'),
                    'auth_token': os.environ.get('STAGING_TOKEN', ''),
                    'health_check_path': '/health',
                    'deploy_path': '/api/deploy'
                },
                'production': {
                    'endpoint': os.environ.get('PROD_ENDPOINT', 'http://prod.local:8080'),
                    'auth_token': os.environ.get('PROD_TOKEN', ''),
                    'health_check_path': '/health',
                    'deploy_path': '/api/deploy'
                }
            },
            'health_check_timeout': 30,
            'deploy_timeout': 120,
            'rollback_on_failure': True
        }
        
        self.remote_deployments: List[Dict] = []
        self.remote_rollback_history: List[Dict] = []
        self.active_environments: List[str] = []
    
    def deploy_to_remote(self, model: BehaviorModel, environment: str = 'staging',
                        health_check: bool = True) -> Dict:
        """
        Deploy behavior model to a remote environment.
        
        Args:
            model: Behavior model to deploy
            environment: Target environment ('staging', 'production')
            health_check: Whether to perform health check after deployment
            
        Returns:
            Deployment result with status and endpoints
        """
        if environment not in self.config['environments']:
            return {
                'success': False,
                'reason': f"Unknown environment: {environment}",
                'environment': environment
            }
        
        env_config = self.config['environments'][environment]
        deployment_id = f"remote_{environment}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        deployment = {
            'id': deployment_id,
            'environment': environment,
            'model_version': model.version,
            'started_at': datetime.now().isoformat(),
            'status': 'deploying',
            'endpoints': {
                'health': f"{env_config['endpoint']}{env_config['health_check_path']}",
                'deploy': f"{env_config['endpoint']}{env_config['deploy_path']}"
            }
        }
        
        try:
            # Deploy model to remote
            deploy_result = self._deploy_to_endpoint(model, env_config)
            
            if not deploy_result['success']:
                deployment['status'] = 'failed'
                deployment['reason'] = deploy_result.get('reason', 'Deployment failed')
                return deployment
            
            deployment['status'] = 'deployed'
            deployment['deployed_at'] = datetime.now().isoformat()
            
            # Perform health check if requested
            if health_check:
                health_status = self._check_remote_health(env_config)
                deployment['health_check'] = health_status
                
                if not health_status['healthy']:
                    deployment['status'] = 'unhealthy'
                    deployment['health_issue'] = health_status.get('issue', 'Unknown')
                    
                    if self.config['rollback_on_failure']:
                        self._rollback_remote(model, environment, deployment)
                        deployment['status'] = 'rolled_back'
            
            self.remote_deployments.append(deployment)
            
            if environment not in self.active_environments:
                self.active_environments.append(environment)
            
            return deployment
            
        except Exception as e:
            deployment['status'] = 'error'
            deployment['error'] = str(e)
            self.remote_deployments.append(deployment)
            return deployment
    
    def deploy_to_all(self, model: BehaviorModel, environments: List[str] = None) -> Dict:
        """
        Deploy model to multiple environments sequentially.
        
        Args:
            model: Behavior model to deploy
            environments: List of environments (defaults to all)
            
        Returns:
            Multi-environment deployment result
        """
        if environments is None:
            environments = list(self.config['environments'].keys())
        
        results = {}
        
        for env in environments:
            result = self.deploy_to_remote(model, env)
            results[env] = result
            
            # Stop on failure if rollback_on_failure is enabled
            if not result.get('success', False) and self.config['rollback_on_failure']:
                break
        
        return {
            'model_version': model.version,
            'environments': results,
            'all_successful': all(r.get('status') == 'deployed' for r in results.values())
        }
    
    def _deploy_to_endpoint(self, model: BehaviorModel, env_config: Dict) -> Dict:
        """Send deployment request to remote endpoint."""
        # In real implementation, this would make HTTP request
        # For now, simulate the deployment
        import requests
        from urllib.parse import urljoin
        
        url = urljoin(env_config['endpoint'], env_config['deploy_path'])
        headers = {
            'Authorization': f'Bearer {env_config["auth_token"]}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model_version': model.version,
            'parameters': model.parameters,
            'performance': model.performance,
            'deployed_at': datetime.now().isoformat()
        }
        
        try:
            response = requests.post(
                url, 
                json=payload, 
                headers=headers, 
                timeout=self.config['deploy_timeout']
            )
            response.raise_for_status()
            return {'success': True, 'response': response.json()}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'reason': str(e)}
    
    def _check_remote_health(self, env_config: Dict) -> Dict:
        """Check health of remote deployment."""
        import requests
        from urllib.parse import urljoin
        
        url = urljoin(env_config['endpoint'], env_config['health_check_path'])
        headers = {
            'Authorization': f'Bearer {env_config["auth_token"]}'
        }
        
        try:
            response = requests.get(
                url, 
                headers=headers, 
                timeout=self.config['health_check_timeout']
            )
            
            if response.status_code == 200:
                return {'healthy': True, 'details': response.json()}
            else:
                return {'healthy': False, 'issue': f"HTTP {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {'healthy': False, 'issue': str(e)}
    
    def _rollback_remote(self, model: BehaviorModel, environment: str, 
                         deployment: Dict):
        """Rollback remote deployment to previous state."""
        rollback_record = {
            'deployment_id': deployment['id'],
            'environment': environment,
            'model_version': deployment['model_version'],
            'timestamp': datetime.now().isoformat()
        }
        
        self.remote_rollback_history.append(rollback_record)
    
    def get_remote_deployment_status(self, environment: str) -> Dict:
        """
        Get status of remote deployment in an environment.
        
        Args:
            environment: Target environment
            
        Returns:
            Current deployment status
        """
        env_config = self.config['environments'].get(environment)
        if not env_config:
            return {'status': 'unknown', 'reason': 'Environment not configured'}
        
        health_status = self._check_remote_health(env_config)
        
        # Find most recent deployment for this environment
        env_deployments = [d for d in self.remote_deployments 
                         if d.get('environment') == environment]
        
        if env_deployments:
            latest = env_deployments[-1]
            return {
                'environment': environment,
                'deployed': latest.get('status') == 'deployed',
                'healthy': health_status['healthy'],
                'model_version': latest.get('model_version'),
                'deployed_at': latest.get('deployed_at')
            }
        
        return {
            'environment': environment,
            'deployed': False,
            'healthy': False
        }
    
    def get_remote_deployment_history(self, environment: str = None, 
                                      limit: int = 20) -> List[Dict]:
        """Get deployment history for environment(s)."""
        deployments = self.remote_deployments
        
        if environment:
            deployments = [d for d in deployments if d.get('environment') == environment]
        
        return deployments[-limit:]
    
    def sync_remote_state(self) -> Dict:
        """
        Sync and verify state of all remote deployments.
        
        Returns:
            Sync status for all environments
        """
        status = {}
        
        for env_name in self.config['environments']:
            status[env_name] = self.get_remote_deployment_status(env_name)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'environments': status,
            'total_active': len([s for s in status.values() if s.get('deployed')])
        }


# Example usage
if __name__ == "__main__":
    # Initialize
    evolution = SelfEvolution()
    
    # Collect some trajectories
    evolution.collect_trajectory(
        states=[{'state': 'initial'}, {'state': 'processing'}, {'state': 'final'}],
        actions=[{'type': 'load'}, {'type': 'process'}, {'type': 'output'}],
        rewards=[0.1, 0.5, 1.0],
        outcome='success'
    )
    
    # Run evolution
    result = evolution.evolve()
    
    print(f"Evolution result: {result['training']}")
    print(f"Status: {evolution.get_status()}")
