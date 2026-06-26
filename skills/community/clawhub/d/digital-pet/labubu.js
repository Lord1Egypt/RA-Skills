/**
 * Labubu 3D 模型定义 - 数字宠物版
 * 高精细度模型，支持多种动画和交互
 */

class Labubu {
    constructor() {
        this.group = new THREE.Group();
        this.headGroup = null;
        this.leftEarGroup = null;
        this.rightEarGroup = null;
        this.tailGroup = null;
        
        this.materials = {};
        this.state = 'idle'; // idle, happy, eating, playing, sleeping
        this.stateTimer = 0;
        
        this.initMaterials();
        this.createModel();
    }

    initMaterials() {
        // 毛发 - 经典棕绿色
        this.materials.fur = new THREE.MeshStandardMaterial({
            color: 0x5a7a4a,
            roughness: 0.9,
            metalness: 0.02
        });

        // 浅色毛发
        this.materials.lightFur = new THREE.MeshStandardMaterial({
            color: 0xc8d8a8,
            roughness: 0.8,
            metalness: 0
        });

        // 眼睛
        this.materials.eye = new THREE.MeshStandardMaterial({
            color: 0x0a0a0a,
            roughness: 0.05,
            metalness: 0.3
        });

        // 眼白
        this.materials.eyeWhite = new THREE.MeshStandardMaterial({
            color: 0xfefefe,
            roughness: 0.1
        });

        // 鼻子
        this.materials.nose = new THREE.MeshStandardMaterial({
            color: 0x1a1a1a,
            roughness: 0.4
        });

        // 牙齿
        this.materials.teeth = new THREE.MeshStandardMaterial({
            color: 0xfffef8,
            roughness: 0.3
        });
    }

    createModel() {
        this.createBody();
        this.createHead();
        this.createEars();
        this.createLimbs();
        this.createTail();
    }

    createBody() {
        // 主体
        const bodyGeo = new THREE.SphereGeometry(1, 64, 64);
        bodyGeo.scale(0.95, 1.15, 0.85);
        const body = new THREE.Mesh(bodyGeo, this.materials.fur);
        body.castShadow = true;
        this.group.add(body);

        // 肚子
        const bellyGeo = new THREE.SphereGeometry(0.7, 64, 64);
        bellyGeo.scale(1, 1.15, 0.55);
        const belly = new THREE.Mesh(bellyGeo, this.materials.lightFur);
        belly.position.set(0, -0.1, 0.6);
        belly.castShadow = true;
        this.group.add(belly);
    }

    createHead() {
        this.headGroup = new THREE.Group();
        this.headGroup.position.set(0, 1.25, 0);
        this.group.add(this.headGroup);

        // 头部
        const headGeo = new THREE.SphereGeometry(0.88, 64, 64);
        headGeo.scale(1.05, 0.95, 0.92);
        const head = new THREE.Mesh(headGeo, this.materials.fur);
        head.castShadow = true;
        this.headGroup.add(head);

        // 脸部
        const faceGeo = new THREE.SphereGeometry(0.72, 64, 64);
        faceGeo.scale(1.05, 0.9, 0.5);
        const face = new THREE.Mesh(faceGeo, this.materials.lightFur);
        face.position.set(0, -0.05, 0.48);
        this.headGroup.add(face);

        this.createEyes();
        this.createNose();
        this.createMouth();
    }

    createEyes() {
        // 左眼
        const leftEyeGroup = new THREE.Group();
        leftEyeGroup.position.set(-0.3, 0.08, 0.72);
        this.headGroup.add(leftEyeGroup);

        const eyeWhiteGeo = new THREE.SphereGeometry(0.2, 32, 32);
        const eyeWhite = new THREE.Mesh(eyeWhiteGeo, this.materials.eyeWhite);
        eyeWhite.scale.set(1, 1, 0.5);
        leftEyeGroup.add(eyeWhite);

        const pupilGeo = new THREE.SphereGeometry(0.12, 32, 32);
        const pupil = new THREE.Mesh(pupilGeo, this.materials.eye);
        pupil.position.z = 0.08;
        leftEyeGroup.add(pupil);

        const highlightGeo = new THREE.SphereGeometry(0.045, 16, 16);
        const highlight = new THREE.Mesh(highlightGeo, this.materials.teeth);
        highlight.position.set(0.05, 0.05, 0.14);
        leftEyeGroup.add(highlight);

        const highlight2Geo = new THREE.SphereGeometry(0.02, 8, 8);
        const highlight2 = new THREE.Mesh(highlight2Geo, this.materials.teeth);
        highlight2.position.set(-0.04, -0.03, 0.12);
        leftEyeGroup.add(highlight2);

        // 右眼
        const rightEyeGroup = leftEyeGroup.clone();
        rightEyeGroup.position.set(0.3, 0.08, 0.72);
        this.headGroup.add(rightEyeGroup);
        
        // 保存眼睛引用用于动画
        this.leftEye = leftEyeGroup;
        this.rightEye = rightEyeGroup;
    }

    createNose() {
        const noseGeo = new THREE.SphereGeometry(0.065, 32, 32);
        const nose = new THREE.Mesh(noseGeo, this.materials.nose);
        nose.position.set(0, -0.06, 0.88);
        nose.scale.set(1.4, 1, 0.9);
        this.headGroup.add(nose);
    }

    createMouth() {
        const mouthGroup = new THREE.Group();
        mouthGroup.position.set(0, -0.3, 0.78);
        this.headGroup.add(mouthGroup);

        // 上排牙齿
        for (let i = 0; i < 3; i++) {
            const toothGeo = new THREE.ConeGeometry(0.05, 0.12, 16);
            const tooth = new THREE.Mesh(toothGeo, this.materials.teeth);
            tooth.position.set((i - 1) * 0.09, 0.02, 0.05);
            tooth.rotation.x = Math.PI;
            mouthGroup.add(tooth);
        }

        // 下排牙齿
        for (let i = 0; i < 3; i++) {
            const toothGeo = new THREE.ConeGeometry(0.04, 0.09, 16);
            const tooth = new THREE.Mesh(toothGeo, this.materials.teeth);
            tooth.position.set((i - 1) * 0.09, -0.08, 0.05);
            mouthGroup.add(tooth);
        }
        
        this.mouth = mouthGroup;
    }

    createEars() {
        // 左耳
        this.leftEarGroup = new THREE.Group();
        this.leftEarGroup.position.set(-0.65, 0.45, 0);
        this.headGroup.add(this.leftEarGroup);

        const earGeo = new THREE.ConeGeometry(0.28, 1.3, 32);
        const leftEar = new THREE.Mesh(earGeo, this.materials.fur);
        leftEar.rotation.z = 0.2;
        leftEar.position.set(0, 0.45, 0);
        leftEar.castShadow = true;
        this.leftEarGroup.add(leftEar);

        const innerEarGeo = new THREE.ConeGeometry(0.18, 0.9, 32);
        const innerEar = new THREE.Mesh(innerEarGeo, this.materials.lightFur);
        innerEar.rotation.z = 0.2;
        innerEar.position.set(0.06, 0.45, 0.08);
        this.leftEarGroup.add(innerEar);

        // 右耳
        this.rightEarGroup = new THREE.Group();
        this.rightEarGroup.position.set(0.65, 0.45, 0);
        this.headGroup.add(this.rightEarGroup);

        const rightEar = leftEar.clone();
        rightEar.rotation.z = -0.2;
        this.rightEarGroup.add(rightEar);

        const rightInnerEar = innerEar.clone();
        rightInnerEar.rotation.z = -0.2;
        rightInnerEar.position.set(-0.06, 0.45, 0.08);
        this.rightEarGroup.add(rightInnerEar);
    }

    createLimbs() {
        this.createArm(-0.9, 0.1, 0.1, 1);
        this.createArm(0.9, 0.1, 0.1, -1);
        this.createLeg(-0.35, -1.05, 0.15);
        this.createLeg(0.35, -1.05, 0.15);
    }

    createArm(x, y, z, direction) {
        const armGroup = new THREE.Group();
        armGroup.position.set(x, y, z);
        this.group.add(armGroup);

        const armGeo = new THREE.CylinderGeometry(0.18, 0.16, 0.5, 32);
        const arm = new THREE.Mesh(armGeo, this.materials.fur);
        arm.rotation.z = direction * 0.35;
        arm.position.set(direction * 0.12, 0.12, 0);
        armGroup.add(arm);

        const upperBallGeo = new THREE.SphereGeometry(0.18, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2);
        const upperBall = new THREE.Mesh(upperBallGeo, this.materials.fur);
        upperBall.rotation.z = direction * 0.35;
        upperBall.position.set(direction * 0.12, 0.37, 0);
        armGroup.add(upperBall);

        const lowerBallGeo = new THREE.SphereGeometry(0.16, 32, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2);
        const lowerBall = new THREE.Mesh(lowerBallGeo, this.materials.fur);
        lowerBall.rotation.z = direction * 0.35;
        lowerBall.position.set(direction * 0.12, -0.13, 0);
        armGroup.add(lowerBall);

        const handGeo = new THREE.SphereGeometry(0.2, 32, 32);
        const hand = new THREE.Mesh(handGeo, this.materials.fur);
        hand.position.set(direction * 0.3, -0.08, 0);
        hand.scale.set(1, 0.9, 0.8);
        armGroup.add(hand);

        for (let i = 0; i < 3; i++) {
            const fingerGeo = new THREE.ConeGeometry(0.04, 0.15, 8);
            const finger = new THREE.Mesh(fingerGeo, this.materials.lightFur);
            finger.position.set(
                direction * (0.35 + (i - 1) * 0.08),
                -0.2,
                (i - 1) * 0.06
            );
            finger.rotation.z = direction * 0.25;
            armGroup.add(finger);
        }
        
        // 保存手臂引用
        if (direction > 0) {
            this.leftArm = armGroup;
        } else {
            this.rightArm = armGroup;
        }
    }

    createLeg(x, y, z) {
        const legGroup = new THREE.Group();
        legGroup.position.set(x, y, z);
        this.group.add(legGroup);

        const thighGeo = new THREE.CylinderGeometry(0.2, 0.18, 0.4, 32);
        const thigh = new THREE.Mesh(thighGeo, this.materials.fur);
        thigh.position.y = -0.1;
        legGroup.add(thigh);

        const upperBallGeo = new THREE.SphereGeometry(0.2, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2);
        const upperBall = new THREE.Mesh(upperBallGeo, this.materials.fur);
        upperBall.position.y = 0.1;
        legGroup.add(upperBall);

        const lowerBallGeo = new THREE.SphereGeometry(0.18, 32, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2);
        const lowerBall = new THREE.Mesh(lowerBallGeo, this.materials.fur);
        lowerBall.position.y = -0.3;
        legGroup.add(lowerBall);

        const footGeo = new THREE.SphereGeometry(0.25, 32, 32);
        footGeo.scale(1, 0.6, 1.2);
        const foot = new THREE.Mesh(footGeo, this.materials.fur);
        foot.position.set(0, -0.45, 0.1);
        legGroup.add(foot);

        for (let i = 0; i < 3; i++) {
            const toeGeo = new THREE.SphereGeometry(0.065, 16, 16);
            const toe = new THREE.Mesh(toeGeo, this.materials.lightFur);
            toe.position.set((i - 1) * 0.12, -0.55, 0.3);
            toe.scale.y = 0.6;
            legGroup.add(toe);
        }
    }

    createTail() {
        this.tailGroup = new THREE.Group();
        this.tailGroup.position.set(0, -0.35, -0.7);
        this.group.add(this.tailGroup);

        for (let i = 0; i < 5; i++) {
            const size = 0.16 - i * 0.02;
            const tailGeo = new THREE.SphereGeometry(size, 32, 32);
            const tail = new THREE.Mesh(tailGeo, this.materials.fur);
            tail.position.set(0, -0.1 * i, -0.06 * i);
            this.tailGroup.add(tail);

            if (i < 4) {
                const connGeo = new THREE.CylinderGeometry(
                    0.16 - (i + 1) * 0.02,
                    0.16 - i * 0.02,
                    0.12,
                    16
                );
                const conn = new THREE.Mesh(connGeo, this.materials.fur);
                conn.position.set(0, -0.05 - 0.1 * i, -0.03 - 0.06 * i);
                conn.rotation.x = -0.5;
                this.tailGroup.add(conn);
            }
        }

        const tipGeo = new THREE.SphereGeometry(0.18, 32, 32);
        const tip = new THREE.Mesh(tipGeo, this.materials.lightFur);
        tip.position.set(0, -0.55, -0.35);
        this.tailGroup.add(tip);
    }

    // 主要动画函数
    animate(time, mouseX, mouseY) {
        this.stateTimer += 0.016;
        
        switch(this.state) {
            case 'idle':
                this.idleAnimation(time);
                break;
            case 'happy':
                this.happyAnimation(time);
                break;
            case 'eating':
                this.eatingAnimation(time);
                break;
            case 'playing':
                this.playAnimation(time);
                break;
            case 'sleeping':
                this.sleepAnimation(time);
                break;
        }
        
        // 耳朵跟随鼠标
        if (this.leftEarGroup && this.rightEarGroup) {
            this.leftEarGroup.rotation.z = 0.2 + mouseX * 0.3;
            this.rightEarGroup.rotation.z = -0.2 + mouseX * 0.3;
            this.leftEarGroup.rotation.x = -mouseY * 0.3;
            this.rightEarGroup.rotation.x = -mouseY * 0.3;
        }
        
        // 尾巴摇摆
        if (this.tailGroup) {
            this.tailGroup.rotation.z = Math.sin(time * 3) * 0.15;
            this.tailGroup.rotation.y = Math.cos(time * 2) * 0.1;
        }
    }

    idleAnimation(time) {
        const scale = 1 + Math.sin(time * 1.8) * 0.012;
        this.group.scale.set(scale, scale, scale);
        this.group.position.y = Math.sin(time * 1.5) * 0.02;
        
        if (this.headGroup) {
            this.headGroup.rotation.z = Math.sin(time * 1) * 0.035;
            this.headGroup.rotation.x = Math.sin(time * 0.7) * 0.025;
        }
    }

    happyAnimation(time) {
        const jump = Math.abs(Math.sin(time * 12)) * 0.3;
        this.group.position.y = jump;
        this.group.scale.set(1.05, 1.05, 1.05);
        
        if (this.headGroup) {
            this.headGroup.rotation.z = Math.sin(time * 15) * 0.1;
            this.headGroup.rotation.y = Math.sin(time * 10) * 0.1;
        }
        
        // 手臂挥舞
        if (this.leftArm && this.rightArm) {
            this.leftArm.rotation.z = Math.sin(time * 15) * 0.5;
            this.rightArm.rotation.z = -Math.sin(time * 15) * 0.5;
        }
        
        if (this.stateTimer > 2) {
            this.state = 'idle';
            this.stateTimer = 0;
            // 重置手臂
            if (this.leftArm && this.rightArm) {
                this.leftArm.rotation.z = 0;
                this.rightArm.rotation.z = 0;
            }
        }
    }

    eatingAnimation(time) {
        // 咀嚼动画
        const chew = Math.sin(time * 8) * 0.05;
        if (this.headGroup) {
            this.headGroup.rotation.x = 0.1 + chew;
        }
        
        // 身体轻微晃动
        this.group.scale.set(1.02, 0.98, 1.02);
        
        if (this.stateTimer > 2) {
            this.state = 'idle';
            this.stateTimer = 0;
        }
    }

    playAnimation(time) {
        // 旋转
        this.group.rotation.y = Math.sin(time * 5) * 0.5;
        
        // 跳跃
        const jump = Math.abs(Math.sin(time * 6)) * 0.4;
        this.group.position.y = jump;
        
        // 挥手
        if (this.leftArm && this.rightArm) {
            this.leftArm.rotation.z = Math.PI - 0.5 + Math.sin(time * 10) * 0.3;
            this.rightArm.rotation.z = -Math.PI + 0.5 - Math.sin(time * 10) * 0.3;
        }
        
        if (this.stateTimer > 3) {
            this.state = 'idle';
            this.stateTimer = 0;
            this.group.rotation.y = 0;
            if (this.leftArm && this.rightArm) {
                this.leftArm.rotation.z = 0;
                this.rightArm.rotation.z = 0;
            }
        }
    }

    sleepAnimation(time) {
        // 缓慢呼吸
        const scale = 1 + Math.sin(time * 0.8) * 0.02;
        this.group.scale.set(scale, scale, scale);
        this.group.position.y = -0.1;
        
        if (this.headGroup) {
            this.headGroup.rotation.x = 0.3;
            this.headGroup.rotation.z = 0;
        }
        
        // 眼睛闭上
        if (this.leftEye && this.rightEye) {
            this.leftEye.scale.y = 0.1;
            this.rightEye.scale.y = 0.1;
        }
    }

    // 交互触发函数
    eatAnimation() {
        this.state = 'eating';
        this.stateTimer = 0;
    }

    playAnimation() {
        this.state = 'playing';
        this.stateTimer = 0;
    }

    petAnimation() {
        this.state = 'happy';
        this.stateTimer = 0;
    }

    sleep() {
        this.state = 'sleeping';
        this.stateTimer = 0;
    }

    wakeUp() {
        this.state = 'idle';
        this.stateTimer = 0;
        // 睁开眼睛
        if (this.leftEye && this.rightEye) {
            this.leftEye.scale.y = 1;
            this.rightEye.scale.y = 1;
        }
        this.group.position.y = 0;
        if (this.headGroup) {
            this.headGroup.rotation.x = 0;
        }
    }

    getMesh() {
        return this.group;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = Labubu;
}
