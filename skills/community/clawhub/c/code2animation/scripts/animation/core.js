// Core time synchronization and basic functionality
export class AnimationCore {
  constructor() {
    this.currentTime = 0;
    this.tasks = [];
    this.nextTaskId = 1;
    
    // Override time functions
    this.originalDateNow = Date.now;
    this.originalPerformanceNow = performance.now;
    
    this.setupTimeOverrides();
  }
  
  setupTimeOverrides() {
    Date.now = () => this.currentTime * 1000;
    if (window.performance) {
      performance.now = () => this.currentTime * 1000;
    }
  }
  
  syncTime(time) {
    // Allow reset to 0, or forward movement
    if (time < this.currentTime && time !== 0) {
      console.log(`[Animation] Ignoring backward seek from ${this.currentTime} to ${time}`);
      return;
    }
    
    // If resetting to 0, clear frame animations
    if (time === 0 && this.currentTime > 0) {
      console.log(`[Animation] Resetting animations`);
      
      // Notify frame animation manager to clear animations
      if (window.frameAnimationManager) {
        window.frameAnimationManager.clearAllAnimations();
      }
    }
    
    console.log(`[Animation] Syncing time from ${this.currentTime} to ${time}`);
    this.currentTime = time;
    
    // Process any tasks (not used in simple version)
    // ...
    
    // Notify parent that we are synced
    window.parent.postMessage({ type: 'iframeSynced', time: time }, '*');
  }
  
  addTask(callback, delay, type = 'timeout') {
    const id = this.nextTaskId++;
    const time = typeof delay === 'number' ? delay : 0;
    const task = { 
      callback, 
      targetTime: this.currentTime + time / 1000, 
      id, 
      type 
    };
    
    if (type === 'interval') {
      task.delay = time / 1000;
    }
    
    this.tasks.push(task);
    return id;
  }
  
  removeTask(id) {
    this.tasks = this.tasks.filter(t => t.id !== id);
  }
}