# Neural Network Architecture Patterns

## Overview

This document provides comprehensive patterns and templates for neural network architectures commonly used in deep learning applications. These patterns can be adapted and combined to create custom neural network architectures for specific use cases.

## Common Architecture Patterns

### 1. Feedforward Neural Networks (FNN)

#### Basic Pattern
```python
from tensorflow.keras import layers, models

def create_feedforward_network(input_shape, output_units):
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=input_shape),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(output_units, activation='softmax')
    ])
    return model
```

#### Variations:
- **Deep FNN**: Add more hidden layers (4-8 layers)
- **Wide FNN**: Increase units per layer (256-512)
- **Bottleneck FNN**: Reduce units in middle layers

#### Use Cases:
- Simple classification tasks
- Regression problems
- Baseline models for comparison

### 2. Convolutional Neural Networks (CNN)

#### Basic CNN Pattern
```python
def create_cnn(input_shape, num_classes):
    model = models.Sequential([
        # Feature extraction
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        
        # Classification
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model
```

#### Advanced CNN Patterns:
- **ResNet-style**: Skip connections
- **Inception-style**: Multi-scale convolutions
- **DenseNet-style**: Dense connections

#### Use Cases:
- Image classification
- Object detection
- Image segmentation
- Medical imaging

### 3. Recurrent Neural Networks (RNN)

#### Basic RNN Pattern
```python
def create_rnn(input_shape, output_units):
    model = models.Sequential([
        layers.SimpleRNN(128, input_shape=input_shape, return_sequences=True),
        layers.Dropout(0.2),
        layers.SimpleRNN(64),
        layers.Dropout(0.2),
        layers.Dense(output_units, activation='softmax')
    ])
    return model
```

#### LSTM Pattern:
```python
def create_lstm(input_shape, output_units):
    model = models.Sequential([
        layers.LSTM(128, input_shape=input_shape, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(64),
        layers.Dropout(0.2),
        layers.Dense(output_units, activation='softmax')
    ])
    return model
```

#### GRU Pattern:
```python
def create_gru(input_shape, output_units):
    model = models.Sequential([
        layers.GRU(128, input_shape=input_shape, return_sequences=True),
        layers.Dropout(0.2),
        layers.GRU(64),
        layers.Dropout(0.2),
        layers.Dense(output_units, activation='softmax')
    ])
    return model
```

#### Use Cases:
- Time series analysis
- Natural language processing
- Speech recognition
- Sequence prediction

### 4. Transformer Networks

#### Basic Transformer Pattern
```python
from tensorflow.keras.layers import MultiHeadAttention, LayerNormalization

def create_transformer(input_shape, num_heads, ff_dim, num_heads):
    inputs = layers.Input(shape=input_shape)
    
    # Multi-head attention
    attention = MultiHeadAttention(num_heads=num_heads, key_dim=ff_dim)
    x = attention(inputs, inputs)
    x = LayerNormalization(epsilon=1e-6)(x + inputs)
    
    # Feed forward
    ffn = layers.Dense(ff_dim, activation='relu')(x)
    ffn = layers.Dense(input_shape[-1])(ffn)
    x = LayerNormalization(epsilon=1e-6)(x + ffn)
    
    # Global average pooling
    x = layers.GlobalAveragePooling1D()(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    return models.Model(inputs=inputs, outputs=outputs)
```

#### Use Cases:
- Natural language processing
- Computer vision
- Multi-modal learning
- Sequence-to-sequence tasks

### 5. Autoencoder Patterns

#### Basic Autoencoder
```python
def create_autoencoder(input_shape, encoding_dim):
    # Encoder
    encoder = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=input_shape),
        layers.Dense(64, activation='relu'),
        layers.Dense(encoding_dim, activation='relu')
    ])
    
    # Decoder
    decoder = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=(encoding_dim,)),
        layers.Dense(128, activation='relu'),
        layers.Dense(input_shape[0], activation='sigmoid')
    ])
    
    # Autoencoder
    autoencoder = models.Sequential([encoder, decoder])
    return autoencoder, encoder, decoder
```

#### Variational Autoencoder:
```python
def create_vae(input_shape, latent_dim):
    # Encoder
    encoder_inputs = layers.Input(shape=input_shape)
    x = layers.Dense(128, activation='relu')(encoder_inputs)
    x = layers.Dense(64, activation='relu')(x)
    
    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)
    
    # Sampling layer
    def sampling(args):
        z_mean, z_log_var = args
        epsilon = tf.random.normal(shape=tf.shape(z_mean))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon
    
    z = layers.Lambda(sampling)([z_mean, z_log_var])
    
    # Decoder
    decoder_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense(64, activation='relu')(decoder_inputs)
    x = layers.Dense(128, activation='relu')(x)
    decoder_outputs = layers.Dense(input_shape[0], activation='sigmoid')(x)
    
    encoder = models.Model(encoder_inputs, [z_mean, z_log_var, z])
    decoder = models.Model(decoder_inputs, decoder_outputs)
    
    return encoder, decoder
```

#### Use Cases:
- Dimensionality reduction
- Anomaly detection
- Data denoising
- Feature learning

### 6. Generative Adversarial Networks (GAN)

#### Basic GAN Pattern
```python
def create_gan(input_shape, latent_dim):
    # Generator
    generator = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(latent_dim,)),
        layers.Dense(256, activation='relu'),
        layers.Dense(512, activation='relu'),
        layers.Dense(np.prod(input_shape), activation='sigmoid'),
        layers.Reshape(input_shape)
    ])
    
    # Discriminator
    discriminator = models.Sequential([
        layers.Flatten(input_shape=input_shape),
        layers.Dense(512, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    # Combined model
    discriminator.compile(optimizer='adam', loss='binary_crossentropy')
    discriminator.trainable = False
    
    gan_input = layers.Input(shape=(latent_dim,))
    gan_output = discriminator(generator(gan_input))
    gan = models.Model(gan_input, gan_output)
    gan.compile(optimizer='adam', loss='binary_crossentropy')
    
    return generator, discriminator, gan
```

#### Use Cases:
- Image generation
- Data augmentation
- Style transfer
- Super-resolution

## Architecture Design Principles

### 1. Layer Configuration Guidelines

#### Hidden Layers:
- **Number**: Start with 2-4 layers, increase for complex problems
- **Units**: Power of 2 (32, 64, 128, 256, 512)
- **Activation**: ReLU for hidden layers, softmax/sigmoid for output
- **Regularization**: Dropout (0.2-0.5), L2 regularization (0.001-0.01)

#### Convolutional Layers:
- **Filters**: Power of 2 (32, 64, 128, 256)
- **Kernel Size**: 3x3 for most cases, larger for larger patterns
- **Stride**: 1 for most cases, 2 for downsampling
- **Padding**: 'same' for preserving dimensions, 'valid' for reducing

#### Recurrent Layers:
- **Units**: 64-256 for most applications
- **Return Sequences**: True for stacked RNNs, False for final layer
- **Dropout**: 0.2-0.5 for regularization

### 2. Network Architecture Patterns

#### Residual Network (ResNet):
```python
def residual_block(x, filters):
    shortcut = x
    x = layers.Conv2D(filters, (3, 3), padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = layers.Conv2D(filters, (3, 3), padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Add()([x, shortcut])
    x = layers.Activation('relu')(x)
    return x
```

#### Inception Module:
```python
def inception_module(x, filters):
    # 1x1 conv
    conv1x1 = layers.Conv2D(filters[0], (1, 1), padding='same')(x)
    
    # 3x3 conv
    conv3x3 = layers.Conv2D(filters[1], (3, 3), padding='same')(x)
    
    # 5x5 conv
    conv5x5 = layers.Conv2D(filters[2], (5, 5), padding='same')(x)
    
    # Max pooling
    maxpool = layers.MaxPooling2D((3, 3), strides=(1, 1), padding='same')(x)
    maxpool = layers.Conv2D(filters[3], (1, 1), padding='same')(maxpool)
    
    # Concatenate
    output = layers.concatenate([conv1x1, conv3x3, conv5x5, maxpool])
    return output
```

### 3. Attention Mechanisms

#### Self-Attention:
```python
def self_attention(x, attention_dim):
    # Query, Key, Value projections
    query = layers.Dense(attention_dim)(x)
    key = layers.Dense(attention_dim)(x)
    value = layers.Dense(attention_dim)(x)
    
    # Attention scores
    attention_scores = layers.Dot(axes=(2, 2))([query, key])
    attention_weights = layers.Activation('softmax')(attention_scores)
    
    # Apply attention
    attended = layers.Dot(axes=(2, 1))([attention_weights, value])
    return attended
```

#### Multi-Head Attention:
```python
def multi_head_attention(x, num_heads, head_dim):
    inputs_split = layers.Lambda(
        lambda x: tf.split(x, num_heads, axis=-1)
    )(x)
    
    attention_heads = []
    for i in range(num_heads):
        attention = self_attention(inputs_split[i], head_dim)
        attention_heads.append(attention)
    
    # Concatenate and project
    concatenated = layers.concatenate(attention_heads)
    output = layers.Dense(x.shape[-1])(concatenated)
    return output
```

## Architecture Selection Guide

### 1. Problem Type Selection

| Problem Type | Recommended Architecture |
|-------------|-------------------------|
| Image Classification | CNN, ResNet, Vision Transformer |
| Object Detection | YOLO, SSD, Faster R-CNN |
| Semantic Segmentation | U-Net, DeepLab, Mask R-CNN |
| Time Series Prediction | LSTM, GRU, Temporal CNN |
| NLP Tasks | Transformer, BERT, GPT |
| Anomaly Detection | Autoencoder, One-Class SVM |
| Generative Tasks | GAN, VAE, Diffusion Models |

### 2. Data Size Considerations

#### Small Datasets (< 10,000 samples):
- Use pre-trained models (transfer learning)
- Apply strong regularization
- Use data augmentation
- Choose simpler architectures

#### Medium Datasets (10,000 - 100,000 samples):
- Use moderate architectures
- Apply moderate regularization
- Use some data augmentation
- Consider ensemble methods

#### Large Datasets (> 100,000 samples):
- Use complex architectures
- Apply minimal regularization
- Use advanced data augmentation
- Consider distributed training

### 3. Computational Constraints

#### Limited Memory:
- Use smaller batch sizes
- Implement gradient checkpointing
- Use model pruning
- Choose efficient architectures

#### Limited GPU:
- Use mixed precision training
- Implement model parallelism
- Choose efficient layers
- Optimize data loading

#### Limited Training Time:
- Use pre-trained models
- Implement early stopping
- Choose efficient architectures
- Use distributed training

## Architecture Optimization Techniques

### 1. Model Compression
- **Pruning**: Remove redundant neurons/connections
- **Quantization**: Reduce precision of weights
- **Knowledge Distillation**: Train smaller models from larger ones

### 2. Architecture Search
- **Grid Search**: Systematic parameter search
- **Random Search**: Random parameter exploration
- **Bayesian Optimization**: Probabilistic parameter optimization

### 3. Ensemble Methods
- **Bagging**: Train multiple models on different subsets
- **Boosting**: Sequential training of models
- **Stacking**: Combine predictions from multiple models

## Implementation Templates

### 1. Template for Custom Architecture
```python
def create_custom_architecture(input_shape, num_classes):
    model = models.Sequential([
        # Input layer
        layers.Input(shape=input_shape),
        
        # Feature extraction
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Classification
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model
```

### 2. Template for Multi-Input Architecture
```python
def create_multi_input_model(input_shapes, num_classes):
    # Input branches
    input1 = layers.Input(shape=input_shapes[0])
    input2 = layers.Input(shape=input_shapes[1])
    
    # Branch 1 processing
    x1 = layers.Dense(128, activation='relu')(input1)
    x1 = layers.Dropout(0.3)(x1)
    
    # Branch 2 processing
    x2 = layers.Conv2D(32, (3, 3), activation='relu')(input2)
    x2 = layers.MaxPooling2D((2, 2))(x2)
    x2 = layers.Flatten()(x2)
    
    # Merge branches
    merged = layers.concatenate([x1, x2])
    merged = layers.Dense(256, activation='relu')(merged)
    merged = layers.Dropout(0.5)(merged)
    
    # Output
    output = layers.Dense(num_classes, activation='softmax')(merged)
    
    return models.Model([input1, input2], output)
```

These patterns and templates provide a solid foundation for building neural network architectures. Remember to adapt them to your specific use case and requirements.