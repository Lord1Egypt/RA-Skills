# Android Gradle 版本兼容矩阵

> 最后更新: 2026-03-28 | 来源: Android Developers 官方文档

## 快速参考：黄金配置

| 配置名 | AGP | Gradle | JDK | Kotlin | 适用场景 |
|--------|-----|--------|-----|--------|---------|
| 稳定版 | 8.7.0 | 8.9 | 17 | 2.0.21 | 生产项目推荐 |
| 最新版 | 9.1.0 | 9.3.1 | 17 | 2.1.0 | 尝鲜新特性 |

## AGP 9.x 系列

| AGP 版本 | 最低 Gradle | 推荐 Gradle | 最低 JDK | SDK Build Tools | 发布时间 |
|----------|------------|------------|---------|----------------|---------|
| 9.1.0 | 9.3.1 | 9.3.1 | 17 | 36.0.0 | 2026-03 |
| 9.0.0 | 9.1.0 | 9.1.0 | 17 | 36.0.0 | 2026-01 |

## AGP 8.x 系列

| AGP 版本 | 最低 Gradle | 最低 JDK |
|----------|------------|---------|
| 8.7.0 | 8.9 | 17 |
| 8.6.0 | 8.7 | 17 |
| 8.5.0 | 8.7 | 17 |
| 8.4.0 | 8.6 | 17 |
| 8.3.0 | 8.4 | 17 |
| 8.2.0 | 8.2 | 17 |
| 8.1.0 | 8.0 | 17 |
| 8.0.0 | 8.0 | 17 |

## AGP 7.x 系列（遗留）

| AGP 版本 | 最低 Gradle | 最低 JDK |
|----------|------------|---------|
| 7.5 | 7.6 | 11 |
| 7.4 | 7.5 | 11 |
| 7.3 | 7.4 | 11 |
| 7.2 | 7.3.3 | 11 |
| 7.1 | 7.2 | 11 |
| 7.0 | 7.0 | 11 |

## Kotlin 与 AGP 兼容性

| Kotlin 版本 | 兼容 AGP 版本 |
|------------|--------------|
| 2.1.x | AGP 8.7+, 9.x |
| 2.0.x | AGP 8.5+, 9.x |
| 1.9.x | AGP 8.0+, 9.x |

## Gradle Wrapper 配置

`gradle/wrapper/gradle-wrapper.properties`:

```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-{VERSION}-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

将 `{VERSION}` 替换为目标 Gradle 版本。

## 验证命令

```bash
# 审计环境
python scripts/detect_env.py

# 检查 Gradle 版本
./gradlew --version

# 检查 JDK 版本
java -version

# 验证编译
./gradlew assembleDebug
```

## 注意事项

1. AGP 8.0+ 强制要求 JDK 17
2. AGP 9.x 要求 Gradle 9.1+
3. stable 配置默认需要 `platforms/android-35` 与匹配的 build-tools
4. 国内环境需配置 Maven 镜像（见 config-templates.md）
5. `JAVA_HOME` 会影响 CLI Gradle 使用的 JDK；未配置时会退回 `PATH`，这会增加环境漂移风险
6. `JAVA_HOME`、Android Studio Gradle JDK、项目级 Gradle JDK 最好保持一致
7. 没有真实 Gradle Wrapper 时，不要宣称项目已验证可构建
8. 版本信息会过时，建议定期查阅官方文档更新
