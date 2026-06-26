// Frame-based animation system
export class FrameAnimationManager {
  constructor(core) {
    this.core = core;
    this.frameAnimations = new Map();
    this.animationId = 0;
  }
  
  // Register frame-based animation
  registerFrameAnimation(element, animationFn, duration = null) {
    const id = this.animationId++;
    this.frameAnimations.set(id, {
      element,
      animationFn,
      startTime: this.core.currentTime,
      duration
    });
    return id;
  }
  
  // Remove animation
  removeFrameAnimation(id) {
    this.frameAnimations.delete(id);
  }
  
  // Clear all animations (for reset)
  clearAllAnimations() {
    console.log(`[Animation] Clearing ${this.frameAnimations.size} frame animations`);
    this.frameAnimations.clear();
  }
  
  // Update all frame animations
  updateAnimations(time) {
    this.frameAnimations.forEach((anim, id) => {
      const elapsed = time - anim.startTime;
      if (elapsed >= 0) {
        if (anim.duration && elapsed > anim.duration) {
          // Animation completed
          this.frameAnimations.delete(id);
        } else {
          // Update animation
          try {
            anim.animationFn(time * 60, elapsed); // Assuming 60fps
          } catch (e) {
            console.error('Animation error:', e);
            this.frameAnimations.delete(id);
          }
        }
      }
    });
  }
}