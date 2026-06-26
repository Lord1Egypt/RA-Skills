/**
 * 声音管理器 - 数字宠物音效
 */

class SoundManager {
    constructor() {
        this.audioContext = null;
        this.enabled = true;
        this.initAudio();
    }
    
    initAudio() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn('Web Audio API 不支持');
            this.enabled = false;
        }
    }
    
    // 播放音效（如果启用）
    play(type) {
        if (!this.enabled || !this.audioContext) return;
        
        // 用户交互后解锁音频上下文
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
        
        switch(type) {
            case 'feed':
                this.playFeedSound();
                break;
            case 'play':
                this.playPlaySound();
                break;
            case 'pet':
                this.playPetSound();
                break;
            case 'happy':
                this.playHappySound();
                break;
            case 'jump':
                this.playJumpSound();
                break;
        }
    }
    
    // 喂食音效 - 可爱的咀嚼声
    playFeedSound() {
        const now = this.audioContext.currentTime;
        
        // 创建多个短音模拟咀嚼
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                const osc = this.audioContext.createOscillator();
                const gain = this.audioContext.createGain();
                
                osc.connect(gain);
                gain.connect(this.audioContext.destination);
                
                osc.frequency.setValueAtTime(800 + Math.random() * 200, now);
                osc.frequency.exponentialRampToValueAtTime(400, now + 0.1);
                
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                
                osc.start(now);
                osc.stop(now + 0.1);
            }, i * 150);
        }
    }
    
    // 玩耍音效 - 开心的音阶
    playPlaySound() {
        const now = this.audioContext.currentTime;
        const frequencies = [523.25, 659.25, 783.99, 1046.50]; // C E G C
        
        frequencies.forEach((freq, i) => {
            const osc = this.audioContext.createOscillator();
            const gain = this.audioContext.createGain();
            
            osc.connect(gain);
            gain.connect(this.audioContext.destination);
            
            osc.frequency.value = freq;
            osc.type = 'sine';
            
            gain.gain.setValueAtTime(0, now + i * 0.1);
            gain.gain.linearRampToValueAtTime(0.2, now + i * 0.1 + 0.05);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.1 + 0.2);
            
            osc.start(now + i * 0.1);
            osc.stop(now + i * 0.1 + 0.2);
        });
    }
    
    // 抚摸音效 - 柔和的上升音
    playPetSound() {
        const now = this.audioContext.currentTime;
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        osc.connect(gain);
        gain.connect(this.audioContext.destination);
        
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.linearRampToValueAtTime(880, now + 0.3);
        osc.type = 'sine';
        
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.25, now + 0.1);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
        
        osc.start(now);
        osc.stop(now + 0.4);
    }
    
    // 开心音效 - 跳跃的音符
    playHappySound() {
        const now = this.audioContext.currentTime;
        const frequencies = [659.25, 523.25, 783.99, 523.25, 1046.50]; // E C G C C'
        
        frequencies.forEach((freq, i) => {
            const osc = this.audioContext.createOscillator();
            const gain = this.audioContext.createGain();
            
            osc.connect(gain);
            gain.connect(this.audioContext.destination);
            
            osc.frequency.value = freq;
            osc.type = 'triangle';
            
            gain.gain.setValueAtTime(0, now + i * 0.08);
            gain.gain.linearRampToValueAtTime(0.3, now + i * 0.08 + 0.02);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.08 + 0.15);
            
            osc.start(now + i * 0.08);
            osc.stop(now + i * 0.08 + 0.15);
        });
    }
    
    // 跳跃音效
    playJumpSound() {
        const now = this.audioContext.currentTime;
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        osc.connect(gain);
        gain.connect(this.audioContext.destination);
        
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.1);
        osc.type = 'sine';
        
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        
        osc.start(now);
        osc.stop(now + 0.15);
    }
    
    // 开关音效
    toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
    }
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SoundManager;
}
