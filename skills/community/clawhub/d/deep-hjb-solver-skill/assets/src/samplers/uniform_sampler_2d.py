"""2D Uniform sampling strategy for problems with x and y coordinates."""

import numpy as np
from .base_sampler import BaseSampler


class UniformSampler2D(BaseSampler):
    """2D Uniform sampling strategy supporting multi-dimensional bounds."""
    
    def __init__(self, config, problem):
        """
        Initialize 2D uniform sampler.
        
        Args:
            config: Configuration object
            problem: Problem object with domain information
        """
        super().__init__(config, problem)
        self.X_oversample = config.X_oversample
        self.t_oversample = config.t_oversample
        self.d = problem.d
        
        # Get domain bounds
        bounds = self.domain_bounds
        self.t_low = bounds['t_low']
        self.t_high = bounds['t_high']
        self.X_low = bounds['X_low']  # numpy array for multi-dim
        self.X_high = bounds['X_high']  # numpy array for multi-dim
        
        # Convert to numpy arrays if not already
        if not isinstance(self.X_low, np.ndarray):
            self.X_low = np.array([self.X_low] * self.d)
        if not isinstance(self.X_high, np.ndarray):
            self.X_high = np.array([self.X_high] * self.d)
    
    def sample(self, nSim_interior, nSim_terminal):
        """
        Sample points uniformly from the 2D domain.
        
        Args:
            nSim_interior: Number of space points in the interior to sample
            nSim_terminal: Number of space points at terminal time to sample
            
        Returns:
            Tuple of (t_interior, X_interior, t_terminal, X_terminal)
            where X_interior and X_terminal have shape [N, d]
        """
        # Interior points
        t_interior = np.random.uniform(
            low=self.t_low - self.t_oversample * (self.t_high - self.t_low),
            high=self.t_high,
            size=[nSim_interior, 1]
        ).astype(np.float32)
        
        # Sample each spatial dimension
        X_coords = []
        for i in range(self.d):
            coord = np.random.uniform(
                low=self.X_low[i] - self.X_oversample * (self.X_high[i] - self.X_low[i]),
                high=self.X_high[i] + self.X_oversample * (self.X_high[i] - self.X_low[i]),
                size=[nSim_interior, 1]
            ).astype(np.float32)
            X_coords.append(coord)
        
        # Combine all dimensions
        X_interior = np.concatenate(X_coords, axis=1)
        
        # Terminal condition points
        t_terminal = self.t_high * np.ones((nSim_terminal, 1)).astype(np.float32)
        
        # Sample terminal X points for each dimension
        X_terminal_coords = []
        for i in range(self.d):
            coord = np.random.uniform(
                low=self.X_low[i],
                high=self.X_high[i],
                size=[nSim_terminal, 1]
            ).astype(np.float32)
            X_terminal_coords.append(coord)
        
        X_terminal = np.concatenate(X_terminal_coords, axis=1)
        
        return t_interior, X_interior, t_terminal, X_terminal
