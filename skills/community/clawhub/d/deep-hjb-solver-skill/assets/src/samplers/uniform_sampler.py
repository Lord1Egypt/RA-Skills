"""Uniform sampling strategy."""

import numpy as np
from .base_sampler import BaseSampler


class UniformSampler(BaseSampler):
    """Uniform sampling strategy with oversampling."""
    
    def __init__(self, config, problem):
        """
        Initialize uniform sampler.
        
        Args:
            config: Configuration object
            problem: Problem object with domain information
        """
        super().__init__(config, problem)
        self.X_oversample = config.X_oversample
        self.t_oversample = config.t_oversample
        self.d = problem.d
        
        # Get domain bounds
        self.t_low = self.domain_bounds['t_low']
        self.t_high = self.domain_bounds['t_high']
        self.X_low = self.domain_bounds['X_low']
        self.X_high = self.domain_bounds['X_high']
    
    def sample(self, nSim_interior, nSim_terminal):
        """
        Sample points uniformly from the domain.
        
        Args:
            nSim_interior: Number of space points in the interior to sample
            nSim_terminal: Number of space points at terminal time to sample
            
        Returns:
            Tuple of (t_interior, X_interior, t_terminal, X_terminal)
        """
        # Interior points
        t_interior = np.random.uniform(
            low=self.t_low - self.t_oversample * (self.t_high - self.t_low),
            high=self.t_high,
            size=[nSim_interior, 1]
        ).astype(np.float32)
        
        X_interior = np.random.uniform(
            low=self.X_low - self.X_oversample * (self.X_high - self.X_low),
            high=self.X_high + self.X_oversample * (self.X_high - self.X_low),
            size=[nSim_interior, self.d]
        ).astype(np.float32)
        
        # Terminal condition points
        t_terminal = self.t_high * np.ones((nSim_terminal, 1)).astype(np.float32)
        X_terminal = np.random.uniform(
            low=self.X_low - self.X_oversample * (self.X_high - self.X_low),
            high=self.X_high + self.X_oversample * (self.X_high - self.X_low),
            size=[nSim_terminal, self.d]
        ).astype(np.float32)
        
        return t_interior, X_interior, t_terminal, X_terminal
