# CocoaPods 集成

**版本**：不写版本号即使用最新；写版本号则锁定。API 以本地头文件为准，类/方法不存在时提示更新 Pod，见 [SKILL.md](../SKILL.md) 规则 5。

## 安装 CocoaPods（未安装时）

```bash
gem sources -l
gem sources --remove https://rubygems.org/
gem sources -a https://gems.ruby-china.com
sudo gem update --system
sudo gem install -n /usr/local/bin cocoapods  # macOS > 10.11
pod setup
```

## Podfile 模板

**仅定位**（BMKLocationKit，无地图）：
```ruby
platform :ios, '9.0'
target 'YourProjectTarget' do
  pod 'BMKLocationKit', '2.1.3'
end
```

**基础地图**（BaiduMapKit，不写版本号即使用最新）：
```ruby
platform :ios, '10.0'
target 'YourProjectTarget' do
    pod 'BaiduMapKit'
    # pod 'BaiduMapKit/Map'
    # pod 'BaiduMapKit/Search'
    # pod 'BaiduMapKit/Utils'
end
```

**步骑行导航**（BaiduWalkNaviKit，含基础地图，步行/骑行实时导航）：
```ruby
platform :ios, '10.0'
target 'YourProjectTarget' do
    pod 'BaiduWalkNaviKit'
end
```
步骑行导航依赖、配置与示例见 [navi.md](navi.md)。

## 常用命令

```bash
pod install          # 安装后用 .xcworkspace 打开
pod repo update
pod update
```

## pod search 找不到类库

```bash
pod setup
rm ~/Library/Caches/CocoaPods/search_index.json
pod search BaiduMapKit   # 或 pod search BMKLocationKit
```

---

## 后续配置

Info.plist、隐私协议弹窗见 [project-config.md](project-config.md)，图片资源见 [assets.md](assets.md)。

**构建报错**：若出现 `Sandbox: bash deny file-write-create .../Pods/resources-to-copy-xxx.txt`，需关闭 User Script Sandboxing，见 [project-config.md](project-config.md) 的「CocoaPods 构建沙盒」小节。
