"""Base class for sampling strategies."""

from abc import ABC, abstractmethod


class BaseSampler(ABC):
    """Base class for sampling strategies."""
    
    def __init__(self, config, problem):
        """
        Initialize sampler with configuration.
        
        Args:
            config: Configuration object
            problem: Problem object with domain information
        """
        self.config = config
        self.problem = problem
        self.domain_bounds = problem.get_domain_bounds()
    
    @abstractmethod
    def sample(self, nSim_interior, nSim_terminal):
        """
        Sample points from the domain.
        
        Args:
            nSim_interior: Number of interior points to sample
            nSim_terminal: Number of terminal points to sample
            
        Returns:
            Tuple of (t_interior, X_interior, t_terminal, X_terminal)
        """
        pass
