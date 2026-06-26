/**
 * GestureScene - 手势控制场景框架 (Three.js版本)
 * 
 * 封装了输入管理（鼠标/手势自动切换）、MediaPipe 手势检测、Three.js 渲染循环。
 * 用户只需要提供一个"物体工厂函数"，返回的对象实现 update()、isDead() 两个方法，
 * 并包含一个 `mesh` 属性（Three.js Mesh 或 Object3D）。
 * 
 * @example
 * const scene = new GestureScene({
 *   create: (x, y, vx, vy) => {
 *     const mesh = new THREE.Mesh(geometry, material);
 *     mesh.position.set(x, y, 0);
 *     return {
 *       mesh,
 *       update() { this.mesh.position.x += this.vx; this.mesh.position.y += this.vy; },
 *       isDead() { return this.mesh.material.opacity <= 0; }
 *     };
 *   }
 * });
 */

class GestureScene {
  /**
   * @param {Object} config
   * @param {Function} config.create - 物体工厂函数 (x, y, vx, vy) => object with mesh, update(), isDead()
   * @param {number} [config.spawnRate=3] - 每帧生成数量
   * @param {number} [config.burstRate=14] - 鼠标按下/快速移动时的爆发数量
   * @param {number} [config.maxObjects=4000] - 物体上限
   * @param {number[]} [config.background=[0.02, 0.02, 0.05]] - 背景色 [r, g, b] (0-1)
   * @param {number} [config.handVelocityScale=1.8] - 手势速度缩放
   * @param {number} [config.handCooldownMs=500] - 手消失后的冷却时间
   * @param {string} [config.title='手势控制'] - 页面标题
   */
  constructor(config) {
    this.config = {
      create: config.create,
      spawnRate: config.spawnRate ?? 3,
      burstRate: config.burstRate ?? 14,
      maxObjects: config.maxObjects ?? 4000,
      background: config.background ?? [0.02, 0.02, 0.05],
      handVelocityScale: config.handVelocityScale ?? 1.8,
      handCooldownMs: config.handCooldownMs ?? 500,
      handSpawnRate: config.handSpawnRate ?? 2,
      handBurstSpeed: config.handBurstSpeed ?? 15,
      title: config.title ?? '手势控制',
      velocitySmoothing: config.velocitySmoothing ?? 0.35,
      minMoveDist: config.minMoveDist ?? 1.5,
    };

    // 状态
    this.objects = [];
    this.pmx = 0;
    this.pmy = 0;
    this.smvx = 0;
    this.smvy = 0;
    this.rawvx = 0;
    this.rawvy = 0;
    this.handDetected = false;
    this.handX = 0;
    this.handY = 0;
    this.lastHandTime = 0;
    this.cursorX = 0;
    this.cursorY = 0;
    this.inputMode = 'mouse';
    this.camActive = false;
    this.mouseIsPressed = false;

    // MediaPipe
    this.mpHands = null;
    this.mpCamera = null;

    // UI 元素
    this.statusEl = null;
    this.camToggleEl = null;
    this.camPreviewEl = null;

    // Three.js 核心
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.animationId = null;

    // 用于将屏幕坐标转换为Three.js世界坐标
    this.raycaster = null;
    this.mouse = null;

    this._init();
  }

  _init() {
    this._createUI();
    this._initThree();
    this._bindEvents();
    this._animate();
    this._loadMediaPipe().then(() => {
      this._tryStartCamera();
    });
  }

  _createUI() {
    const style = document.createElement('style');
    style.textContent = `
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { background: #08080c; overflow: hidden; }
      canvas { display: block; cursor: none; }
      #cam-preview {
        position: fixed;
        bottom: 16px;
        right: 16px;
        width: 200px;
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.15);
        z-index: 10;
        transform: scaleX(-1);
        display: none;
      }
      #cam-preview.active { display: block; }
      #status {
        position: fixed;
        top: 16px;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255,255,255,0.5);
        font-family: system-ui, sans-serif;
        font-size: 14px;
        z-index: 10;
        pointer-events: none;
        transition: opacity 0.5s;
        white-space: nowrap;
      }
      #cam-toggle {
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 20;
        padding: 8px 18px;
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 8px;
        background: rgba(255,255,255,0.08);
        color: rgba(255,255,255,0.7);
        font-family: system-ui, sans-serif;
        font-size: 14px;
        cursor: pointer;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: all 0.2s;
        display: none;
      }
      #cam-toggle:hover {
        background: rgba(255,255,255,0.15);
        color: #fff;
      }
      #cam-toggle.on {
        border-color: rgba(100,220,255,0.5);
        color: rgba(100,220,255,0.9);
      }
    `;
    document.head.appendChild(style);

    document.title = this.config.title;

    this.camPreviewEl = document.createElement('video');
    this.camPreviewEl.id = 'cam-preview';
    this.camPreviewEl.autoplay = true;
    this.camPreviewEl.playsInline = true;
    this.camPreviewEl.muted = true;
    document.body.appendChild(this.camPreviewEl);

    this.camToggleEl = document.createElement('button');
    this.camToggleEl.id = 'cam-toggle';
    this.camToggleEl.textContent = '关闭摄像头';
    this.camToggleEl.addEventListener('click', () => this.toggleCamera());
    document.body.appendChild(this.camToggleEl);

    this.statusEl = document.createElement('div');
    this.statusEl.id = 'status';
    this.statusEl.textContent = '正在加载…';
    document.body.appendChild(this.statusEl);
  }

  _initThree() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(this.config.background[0], this.config.background[1], this.config.background[2]);

    const aspect = window.innerWidth / window.innerHeight;
    const frustumSize = 1000;
    this.camera = new THREE.OrthographicCamera(
      -frustumSize * aspect / 2,
      frustumSize * aspect / 2,
      frustumSize / 2,
      -frustumSize / 2,
      0.1,
      2000
    );
    this.camera.position.z = 1000;

    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.body.appendChild(this.renderer.domElement);

    this.pmx = 0;
    this.pmy = 0;
    this.handX = 0;
    this.handY = 0;
    this.cursorX = 0;
    this.cursorY = 0;

    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();

    this.statusEl.textContent = '鼠标控制中 · 请伸出手';
  }

  _bindEvents() {
    window.addEventListener('mousemove', (e) => {
      this._updateMousePosition(e.clientX, e.clientY);
    });

    window.addEventListener('mousedown', () => {
      this.mouseIsPressed = true;
    });

    window.addEventListener('mouseup', () => {
      this.mouseIsPressed = false;
    });

    window.addEventListener('resize', () => this._onWindowResize());
  }

  _updateMousePosition(clientX, clientY) {
    const aspect = window.innerWidth / window.innerHeight;
    const frustumSize = 1000;
    
    this.mouse.x = (clientX / window.innerWidth) * frustumSize * aspect - frustumSize * aspect / 2;
    this.mouse.y = -(clientY / window.innerHeight) * frustumSize + frustumSize / 2;
  }

  _onWindowResize() {
    const aspect = window.innerWidth / window.innerHeight;
    const frustumSize = 1000;
    
    this.camera.left = -frustumSize * aspect / 2;
    this.camera.right = frustumSize * aspect / 2;
    this.camera.top = frustumSize / 2;
    this.camera.bottom = -frustumSize / 2;
    
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  _animate() {
    this.animationId = requestAnimationFrame(() => this._animate());

    this._updateInputMode();
    this._updateStatus();
    this._updateVelocity();
    this._spawnObjects();

    this.pmx = this.cursorX;
    this.pmy = this.cursorY;

    for (let i = this.objects.length - 1; i >= 0; i--) {
      const obj = this.objects[i];
      obj.update();
      if (obj.isDead()) {
        if (obj.mesh) {
          this.scene.remove(obj.mesh);
          if (obj.mesh.geometry) obj.mesh.geometry.dispose();
          if (obj.mesh.material) {
            if (Array.isArray(obj.mesh.material)) {
              obj.mesh.material.forEach(m => m.dispose());
            } else {
              obj.mesh.material.dispose();
            }
          }
        }
        this.objects.splice(i, 1);
      }
    }

    while (this.objects.length > this.config.maxObjects) {
      const obj = this.objects.shift();
      if (obj.mesh) {
        this.scene.remove(obj.mesh);
        if (obj.mesh.geometry) obj.mesh.geometry.dispose();
        if (obj.mesh.material) {
          if (Array.isArray(obj.mesh.material)) {
            obj.mesh.material.forEach(m => m.dispose());
          } else {
            obj.mesh.material.dispose();
          }
        }
      }
    }

    this.renderer.render(this.scene, this.camera);
  }

  _updateInputMode() {
    const now = performance.now();

    if (this.handDetected && this.camActive) {
      this.inputMode = 'hand';
      this.cursorX = this.handX;
      this.cursorY = this.handY;
    } else if (this.camActive && (now - this.lastHandTime) < this.config.handCooldownMs) {
      this.inputMode = 'hand';
      this.cursorX = this.handX;
      this.cursorY = this.handY;
    } else {
      this.inputMode = 'mouse';
      this.cursorX = this.mouse.x;
      this.cursorY = this.mouse.y;
    }
  }

  _updateStatus() {
    if (this.camActive) {
      if (this.inputMode === 'hand') {
        this.statusEl.textContent = '✋ 手势控制中';
        this.statusEl.style.color = 'rgba(100,220,255,0.7)';
      } else {
        this.statusEl.textContent = '🖱 鼠标控制中 · 请伸出手';
        this.statusEl.style.color = 'rgba(255,255,255,0.5)';
      }
    }
    this.statusEl.style.opacity = '1';
  }

  _updateVelocity() {
    let rawVx = this.cursorX - this.pmx;
    let rawVy = this.cursorY - this.pmy;

    if (this.inputMode === 'hand') {
      const d = Math.sqrt(rawVx * rawVx + rawVy * rawVy);
      if (d < this.config.minMoveDist) {
        rawVx = 0;
        rawVy = 0;
      }
      this.rawvx = rawVx;
      this.rawvy = rawVy;
      const sf = Math.min(this.config.velocitySmoothing, 0.35);
      this.smvx = this.smvx * (1 - sf) + rawVx * sf;
      this.smvy = this.smvy * (1 - sf) + rawVy * sf;
    } else {
      this.rawvx = rawVx;
      this.rawvy = rawVy;
      this.smvx = rawVx;
      this.smvy = rawVy;
    }
  }

  _spawnObjects() {
    const vx = this.inputMode === 'hand' ? this.smvx * this.config.handVelocityScale : this.smvx;
    const vy = this.inputMode === 'hand' ? this.smvy * this.config.handVelocityScale : this.smvy;

    const detectVx = this.inputMode === 'hand' ? this.rawvx : this.smvx;
    const detectVy = this.inputMode === 'hand' ? this.rawvy : this.smvy;
    const hasMotion = this.inputMode === 'hand'
      ? (Math.abs(detectVx) > 0.5 || Math.abs(detectVy) > 0.5)
      : (detectVx !== 0 || detectVy !== 0);

    if (hasMotion) {
      let rate = this.config.spawnRate;
      if (this.inputMode === 'mouse' && this.mouseIsPressed) {
        rate = this.config.burstRate;
      }
      if (this.inputMode === 'hand') {
        rate = this.config.handSpawnRate;
        const speed = Math.sqrt(vx * vx + vy * vy);
        if (speed > this.config.handBurstSpeed) rate = this.config.burstRate;
      }

      for (let i = 0; i < rate; i++) {
        const t = rate > 1 ? i / (rate - 1) : 0.5;
        const bias = this.inputMode === 'hand' ? 0.85 : 0.5;
        const interpT = t * bias;
        const px = this.pmx + (this.cursorX - this.pmx) * interpT;
        const py = this.pmy + (this.cursorY - this.pmy) * interpT;
        
        const obj = this.config.create(px, py, vx, vy);
        if (obj && obj.mesh) {
          this.scene.add(obj.mesh);
          this.objects.push(obj);
        }
      }
    }
  }

  async _loadMediaPipe() {
    try {
      if (typeof Hands === 'undefined') {
        await this._loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/hands.js');
      }
      if (typeof Camera === 'undefined') {
        await this._loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils@0.3.1675466862/camera_utils.js');
      }
    } catch (error) {
      console.warn('MediaPipe 加载失败，仅支持鼠标控制:', error);
    }
  }

  _loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.crossOrigin = 'anonymous';
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  async toggleCamera() {
    if (this.camActive) {
      this.stopCamera();
    } else {
      await this.startCamera();
    }
  }

  async startCamera() {
    if (typeof Hands === 'undefined') {
      this.statusEl.textContent = 'MediaPipe 未加载，仅支持鼠标控制';
      return;
    }

    this.statusEl.textContent = '正在加载手势模型…';

    try {
      this.mpHands = new Hands({
        locateFile: (file) =>
          `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/${file}`,
      });

      this.mpHands.setOptions({
        maxNumHands: 1,
        modelComplexity: 0,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.4,
      });

      this.mpHands.onResults((results) => this._onHandResults(results));

      this.statusEl.textContent = '正在启动摄像头…';

      this.mpCamera = new Camera(this.camPreviewEl, {
        onFrame: async () => {
          await this.mpHands.send({ image: this.camPreviewEl });
        },
        width: 640,
        height: 480,
      });

      await this.mpCamera.start();

      this.camActive = true;
      this.camPreviewEl.classList.add('active');
      this.camToggleEl.style.display = 'block';
      this.camToggleEl.textContent = '关闭摄像头';
      this.camToggleEl.classList.add('on');
      this.statusEl.textContent = '鼠标控制中 · 请伸出手';
    } catch (error) {
      console.warn('摄像头启动失败:', error);
      this._handleCameraError(error);
    }
  }

  _handleCameraError(error) {
    let message = '鼠标控制中（摄像头不可用）';
    if (error.name === 'NotAllowedError' || 
        (error.message && error.message.includes('Permission denied'))) {
      message = '鼠标控制中（摄像头权限被拒绝）';
    } else if (error.name === 'NotFoundError' || 
               (error.message && error.message.includes('Requested device not found'))) {
      message = '鼠标控制中（未找到摄像头设备）';
    } else if (error.name === 'NotReadableError' || 
               (error.message && error.message.includes('Could not start video source'))) {
      message = '鼠标控制中（摄像头被占用）';
    }
    
    this.statusEl.textContent = message;
    this.camActive = false;
    this.inputMode = 'mouse';
    
    this.cursorX = this.mouse.x;
    this.cursorY = this.mouse.y;
  }

  async _tryStartCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      this.statusEl.textContent = '鼠标控制中（浏览器不支持摄像头）';
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      stream.getTracks().forEach(track => track.stop());
      await this.startCamera();
    } catch (error) {
      console.warn('摄像头权限检测失败:', error);
      this._handleCameraError(error);
    }
  }

  stopCamera() {
    if (this.mpCamera) {
      this.mpCamera.stop();
      this.mpCamera = null;
    }

    this.camPreviewEl.srcObject = null;
    this.camPreviewEl.classList.remove('active');
    this.camActive = false;
    this.handDetected = false;

    this.camToggleEl.textContent = '开启摄像头';
    this.camToggleEl.classList.remove('on');
    this.statusEl.style.opacity = '1';
    this.statusEl.textContent = '鼠标控制中 · 请伸出手';
  }

  _onHandResults(results) {
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
      const tip = results.multiHandLandmarks[0][8];
      
      const aspect = window.innerWidth / window.innerHeight;
      const frustumSize = 1000;
      
      this.handX = (1 - tip.x) * frustumSize * aspect - frustumSize * aspect / 2;
      this.handY = -(tip.y * frustumSize - frustumSize / 2);
      
      this.lastHandTime = performance.now();

      if (!this.handDetected) {
        this.handDetected = true;
        this.pmx = this.handX;
        this.pmy = this.handY;
      }
    } else {
      this.handDetected = false;
    }
  }

  destroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    
    this.objects.forEach(obj => {
      if (obj.mesh) {
        this.scene.remove(obj.mesh);
        if (obj.mesh.geometry) obj.mesh.geometry.dispose();
        if (obj.mesh.material) {
          if (Array.isArray(obj.mesh.material)) {
            obj.mesh.material.forEach(m => m.dispose());
          } else {
            obj.mesh.material.dispose();
          }
        }
      }
    });
    this.objects = [];
    
    this.stopCamera();
    
    if (this.renderer) {
      this.renderer.dispose();
      this.renderer.domElement.remove();
    }
  }
}