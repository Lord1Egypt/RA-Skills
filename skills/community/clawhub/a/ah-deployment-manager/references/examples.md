# Deployment Manager — Code Examples

## Example 1

```javascript
// Feature flag service integration
class FeatureFlagService {
  constructor(flagProvider) {
    this.provider = flagProvider;
  }

  async isEnabled(flagKey, user, defaultValue = false) {
    try {
      return await this.provider.getBooleanValue(flagKey, user, defaultValue);
    } catch (error) {
      console.error(`Feature flag error for ${flagKey}:`, error);
      return defaultValue;
    }
  }

  async getRolloutPercentage(flagKey, defaultValue = 0) {
    try {
      return await this.provider.getNumberValue(flagKey, {}, defaultValue);
    } catch (error) {
      console.error(`Rollout percentage error for ${flagKey}:`, error);
      return defaultValue;
    }
  }
}

// Usage in deployment
const deploymentController = {
  async deployCanary(version, targetPercentage) {
    // Update feature flag for canary percentage
    await featureFlags.updateFlag('canary-percentage', targetPercentage);
    
    // Deploy canary version
    await this.deployVersion(version, 'canary');
    
    // Monitor metrics
    const metrics = await this.monitorCanary(30); // 30 minutes
    
    if (metrics.errorRate < 0.1 && metrics.latencyP99 < 500) {
      return this.promoteCanary();
    } else {
      return this.rollbackCanary();
    }
  }
};
```
