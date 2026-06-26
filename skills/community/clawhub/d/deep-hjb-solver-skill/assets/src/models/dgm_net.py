"""Deep Galerkin Method Neural Network Implementation."""

import tensorflow as tf


class DenseLayer(tf.keras.layers.Layer):
    """Custom dense layer with configurable activation functions."""
    
    def __init__(self, output_dim, input_dim, transformation=None):
        """
        Initialize a dense layer.
        
        Args:
            input_dim: Dimensionality of input data
            output_dim: Number of outputs for dense layer
            transformation: Activation function used inside the layer;
                          None is equivalent to the identity map
        
        Returns: 
            Customized Keras (fully connected) layer object 
        """        
        super(DenseLayer, self).__init__()
        self.output_dim = output_dim
        self.input_dim = input_dim
        
        self.W = self.add_weight(
            name="W",
            shape=[self.input_dim, self.output_dim],
            initializer=tf.initializers.GlorotUniform(),
            dtype=tf.float32
        )
        
        self.b = self.add_weight(
            name="b",
            shape=[1, self.output_dim],
            initializer=tf.zeros_initializer(),
            dtype=tf.float32
        )
        
        if transformation:
            if transformation == "tanh":
                self.transformation = tf.tanh
            elif transformation == "relu":
                self.transformation = tf.nn.relu
            elif transformation == "mish":
                self.transformation = lambda x: x * tf.math.tanh(tf.math.softplus(x))
            elif transformation == "swish":
                self.transformation = lambda x: x * tf.math.sigmoid(x)
            else:
                self.transformation = None
        else:
            self.transformation = None

    def call(self, X):
        """
        Compute output of a dense layer for a given input X.
        
        Args:                        
            X: Input to layer            
        """
        S = tf.add(tf.matmul(X, self.W), self.b)
                
        if self.transformation:
            S = self.transformation(S)
        
        return S


class DGMNet(tf.keras.Model):
    """Deep Galerkin Method Network."""
    
    def __init__(self, layer_width, n_layers, input_dim, 
                 final_trans=None, feedforward=False, 
                 output_dim=1, control_output=False,
                 activation='swish', problem=None):
        """
        Initialize DGM Network.
        
        Args:
            layer_width: Width of hidden layers
            n_layers: Number of hidden layers
            input_dim: Input dimension (spatial dimension)
            final_trans: Final activation function
            feedforward: Whether to use feedforward architecture
            output_dim: Output dimension
            control_output: Whether this is a control network
            activation: Activation function for hidden layers
            problem: Problem object (for value networks to access terminal condition)
        """
        super(DGMNet, self).__init__()

        self.n_layers = n_layers
        self.feedforward = feedforward
        self.output_dim = output_dim
        self.control_output = control_output
        self.input_dim = input_dim
        self.problem = problem

        # Initial layer (includes time dimension)
        self.initial_layer = DenseLayer(
            layer_width, 
            input_dim + 1, 
            transformation=activation
        )

        # Define kernel layers
        self.kernel_layers = []
        for _ in range(n_layers):
            self.kernel_layers.append(
                DenseLayer(layer_width, layer_width, transformation=activation)
            )

        # Final output layer
        self.output_weight = tf.keras.layers.Dense(
            output_dim, 
            activation=final_trans
        )

    def call(self, t, x, training=False):
        """
        Forward pass through the network.
        
        Args:
            t: Time tensor, shape (batch_size, 1)
            x: Space tensor, shape (batch_size, input_dim)
            training: Whether in training mode
            
        Returns:
            Network output
        """
        # Concatenate time and space
        X = tf.concat([t, x], axis=1)
        S = self.initial_layer.call(X)
        
        # Residual connections through hidden layers
        for i in range(self.n_layers):
            S = self.kernel_layers[i](S) + S

        # Final output
        result = self.output_weight(S)
        
        # Apply terminal condition transformation if value network and problem provided
        # This embeds the terminal condition: V(t,x) = g(x) + u(t,x) * (1-t)
        # This ensures V(T,x) = g(x) exactly, making L3 = 0
        if not self.control_output and self.problem is not None:
            terminal_value = self.problem.get_terminal_condition(x)
            result = terminal_value + result * (1 - t)

        return result
