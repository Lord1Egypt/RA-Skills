// Interpolation utility functions
export function interpolate(input, inputRange, outputRange, options = {}) {
  const { extrapolateLeft = 'extend', extrapolateRight = 'extend' } = options;
  
  if (inputRange.length !== outputRange.length) {
    throw new Error('Input and output ranges must have the same length');
  }
  
  // Handle single point
  if (inputRange.length === 1) {
    return outputRange[0];
  }
  
  // Find the correct segment
  let i = 0;
  while (i < inputRange.length - 1 && input > inputRange[i + 1]) {
    i++;
  }
  
  // Handle extrapolation
  if (input < inputRange[0]) {
    if (extrapolateLeft === 'clamp') return outputRange[0];
    if (extrapolateLeft === 'extend') {
      const slope = (outputRange[1] - outputRange[0]) / (inputRange[1] - inputRange[0]);
      return outputRange[0] + slope * (input - inputRange[0]);
    }
  }
  
  if (input > inputRange[inputRange.length - 1]) {
    if (extrapolateRight === 'clamp') return outputRange[outputRange.length - 1];
    if (extrapolateRight === 'extend') {
      const lastIndex = inputRange.length - 1;
      const slope = (outputRange[lastIndex] - outputRange[lastIndex - 1]) / 
                   (inputRange[lastIndex] - inputRange[lastIndex - 1]);
      return outputRange[lastIndex] + slope * (input - inputRange[lastIndex]);
    }
  }
  
  // Linear interpolation
  const progress = (input - inputRange[i]) / (inputRange[i + 1] - inputRange[i]);
  return outputRange[i] + progress * (outputRange[i + 1] - outputRange[i]);
}