/**
 * Three.js 场景设置 - 精致版
 * 更好的光照、阴影和后期效果
 */

let scene, camera, renderer, controls;
let labubu;
let isAutoRotating = true;
let animationId;

function init() {
    const canvas = document.getElementById('canvas');
    const container = document.getElementById('container');

    // 创建场景
    scene = new THREE.Scene();
    scene.background = null;
    
    // 添加雾效增加深度感
    scene.fog = new THREE.Fog(0x667eea, 8, 25);

    // 创建相机
    const aspect = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(40, aspect, 0.1, 1000);
    camera.position.set(0, 0.8, 7);

    // 创建渲染器 - 更高质量
    renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true,
        alpha: true,
        powerPreference: "high-performance"
    });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;

    // 添加光照
    setupLighting();

    // 创建Labubu模型
    labubu = new Labubu();
    const labubuMesh = labubu.getMesh();
    labubuMesh.traverse(child => {
        if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
        }
    });
    scene.add(labubuMesh);

    // 添加地面和环境
    createEnvironment();

    // 添加轨道控制器
    controls = new THREE.OrbitControls(camera, canvas);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 4;
    controls.maxDistance = 12;
    controls.target.set(0, 0.3, 0);
    controls.autoRotate = true;
    controls.autoRotateSpeed = 1.5;
    controls.enablePan = true;
    controls.enableZoom = true;

    // 事件监听
    window.addEventListener('resize', onWindowResize);
    setupUIControls();

    // 开始动画循环
    animate();
}

function setupLighting() {
    // 环境光 - 基础照明
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    // 主光源 - 产生主阴影
    const mainLight = new THREE.DirectionalLight(0xfff4e6, 1.0);
    mainLight.position.set(4, 8, 5);
    mainLight.castShadow = true;
    mainLight.shadow.mapSize.width = 4096;
    mainLight.shadow.mapSize.height = 4096;
    mainLight.shadow.camera.near = 0.1;
    mainLight.shadow.camera.far = 50;
    mainLight.shadow.camera.left = -5;
    mainLight.shadow.camera.right = 5;
    mainLight.shadow.camera.top = 5;
    mainLight.shadow.camera.bottom = -5;
    mainLight.shadow.bias = -0.0001;
    mainLight.shadow.radius = 2;
    scene.add(mainLight);

    // 补光 - 左侧柔光
    const fillLight = new THREE.DirectionalLight(0xddeeff, 0.4);
    fillLight.position.set(-5, 3, 3);
    scene.add(fillLight);

    // 轮廓光 - 后方蓝色调
    const rimLight = new THREE.SpotLight(0xffddcc, 0.6);
    rimLight.position.set(0, 5, -6);
    rimLight.lookAt(0, 0, 0);
    rimLight.penumbra = 0.5;
    scene.add(rimLight);

    // 底部补光 - 减少阴影黑色
    const bottomLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.35);
    scene.add(bottomLight);
    
    // 点缀光 - 增加立体感
    const accentLight = new THREE.PointLight(0xffeecc, 0.3, 10);
    accentLight.position.set(2, 2, 3);
    scene.add(accentLight);
}

function createEnvironment() {
    // 地面阴影接收器
    const groundGeometry = new THREE.PlaneGeometry(30, 30);
    const groundMaterial = new THREE.ShadowMaterial({
        opacity: 0.15,
        color: 0x2a1a4a
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -2;
    ground.receiveShadow = true;
    scene.add(ground);

    // 圆形展示台
    const platformGroup = new THREE.Group();
    scene.add(platformGroup);

    // 台面
    const platformTopGeo = new THREE.CylinderGeometry(2.2, 2.2, 0.15, 64);
    const platformTopMat = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        roughness: 0.15,
        metalness: 0.1
    });
    const platformTop = new THREE.Mesh(platformTopGeo, platformTopMat);
    platformTop.position.y = -2.05;
    platformTop.receiveShadow = true;
    platformTop.castShadow = true;
    platformGroup.add(platformTop);

    // 台边
    const platformEdgeGeo = new THREE.TorusGeometry(2.2, 0.08, 16, 64);
    const platformEdgeMat = new THREE.MeshStandardMaterial({
        color: 0xe0e0e0,
        roughness: 0.2,
        metalness: 0.3
    });
    const platformEdge = new THREE.Mesh(platformEdgeGeo, platformEdgeMat);
    platformEdge.rotation.x = -Math.PI / 2;
    platformEdge.position.y = -1.975;
    platformGroup.add(platformEdge);

    // 台底座
    const platformBaseGeo = new THREE.CylinderGeometry(2.4, 2.6, 0.3, 64);
    const platformBaseMat = new THREE.MeshStandardMaterial({
        color: 0xf5f5f5,
        roughness: 0.3,
        metalness: 0.05
    });
    const platformBase = new THREE.Mesh(platformBaseGeo, platformBaseMat);
    platformBase.position.y = -2.3;
    platformBase.receiveShadow = true;
    platformGroup.add(platformBase);

    // 添加漂浮粒子效果
    createParticles();
}

function createParticles() {
    const particleCount = 50;
    const particles = new THREE.Group();
    
    for (let i = 0; i < particleCount; i++) {
        const size = Math.random() * 0.05 + 0.02;
        const particleGeo = new THREE.SphereGeometry(size, 8, 8);
        const particleMat = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            transparent: true,
            opacity: Math.random() * 0.3 + 0.1
        });
        const particle = new THREE.Mesh(particleGeo, particleMat);
        
        particle.position.set(
            (Math.random() - 0.5) * 10,
            Math.random() * 6 - 1,
            (Math.random() - 0.5) * 6
        );
        
        particle.userData = {
            speedY: Math.random() * 0.01 + 0.002,
            speedX: (Math.random() - 0.5) * 0.005,
            speedZ: (Math.random() - 0.5) * 0.005,
            initialY: particle.position.y
        };
        
        particles.add(particle);
    }
    
    particles.name = 'particles';
    scene.add(particles);
}

function updateParticles() {
    const particles = scene.getObjectByName('particles');
    if (particles) {
        particles.children.forEach(particle => {
            particle.position.y += particle.userData.speedY;
            particle.position.x += particle.userData.speedX;
            particle.position.z += particle.userData.speedZ;
            
            if (particle.position.y > 5) {
                particle.position.y = -1;
            }
            
            // 闪烁效果
            particle.material.opacity = 0.1 + Math.sin(Date.now() * 0.001 + particle.position.x) * 0.1;
        });
    }
}

function onWindowResize() {
    const container = document.getElementById('container');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

function setupUIControls() {
    const toggleBtn = document.getElementById('toggle-rotate');
    const resetBtn = document.getElementById('reset-view');

    toggleBtn.addEventListener('click', () => {
        isAutoRotating = !isAutoRotating;
        controls.autoRotate = isAutoRotating;
        toggleBtn.textContent = isAutoRotating ? '暂停旋转' : '开始旋转';
    });

    resetBtn.addEventListener('click', () => {
        controls.reset();
        camera.position.set(0, 0.8, 7);
        controls.target.set(0, 0.3, 0);
    });
}

function animate() {
    animationId = requestAnimationFrame(animate);

    const time = Date.now() * 0.001;

    // Labubu动画
    if (labubu) {
        labubu.breathe(time);
        labubu.swayHead(time);
        labubu.wagTail(time);
    }

    // 粒子动画
    updateParticles();

    // 更新控制器
    controls.update();

    // 渲染
    renderer.render(scene, camera);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
