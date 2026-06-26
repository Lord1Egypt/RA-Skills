# Java / Spring Boot 检测规则库 — v1.0

> 本文件是 Code Health Scanner 的完整检测规则目录。所有规则按严重度分为 Critical（🔴）、Warning（🟡）和 Info（🟢）三级。

---

## 🔴 Critical Rules

### C-SEC-001: SQL 注入 — MyBatis `${}` 拼接

- **严重度:** Critical
- **分类:** Security
- **检测模式:** 在 `@Select` / `@Update` / `@Insert` / `@Delete` 注解或 XML mapper 中包含 `${...}` 表达式
- **风险说明:** `${}` 是文本替换而非参数绑定，攻击者可注入恶意 SQL 语句，绕过认证、窃取数据或执行 DDL 操作。
- **检测示例:**
  ```java
  // ❌ 危险：用户输入直接拼入 SQL
  @Select("SELECT * FROM user WHERE name = '${name}'")
  User findByName(@Param("name") String name);
  ```
  ```xml
  <!-- ❌ 危险：XML 中的 ${} 拼接 -->
  <select id="findByName" resultType="User">
      SELECT * FROM user WHERE name LIKE '%${name}%'
  </select>
  ```
- **修复建议:** 统一使用 `#{}` 参数占位符，MyBatis 会自动预编译。
  ```java
  // ✅ 安全：使用 #{} 预编译占位
  @Select("SELECT * FROM user WHERE name = #{name}")
  User findByName(@Param("name") String name);
  ```
  ```xml
  <!-- ✅ 安全：使用 #{}，LIKE 查询用 CONCAT 或数据库函数拼接 -->
  <select id="findByName" resultType="User">
      SELECT * FROM user WHERE name LIKE CONCAT('%', #{name}, '%')
  </select>
  ```
- **扣分:** -15
- **误报场景:** 动态 `ORDER BY` 或 `IN` 子句中确实需要动态 SQL 时（应做白名单校验而非直接拼接）。

---

### C-SEC-002: 硬编码密钥/密码

- **严重度:** Critical
- **分类:** Security
- **检测模式:** 源码或配置文件中包含明文密码、API key、token、JWT secret、数据库连接密码等敏感信息
- **风险说明:** 密钥随源码进入 Git 仓库后无法彻底删除历史记录；即使仓库设为 private，任何有仓库访问权限的人员均可获取。一旦泄露可能导致数据泄露、资源滥用。
- **检测示例:**
  ```java
  // ❌ 危险：JWT Secret 硬编码在代码中
  public class JwtConfig {
      private static final String SECRET = "my-secret-key-12345";
      private static final long EXPIRATION = 86400000L;
  }
  ```
  ```yaml
  # ❌ 危险：application.yml 中明文密码
  spring:
    datasource:
      url: jdbc:mysql://localhost:3306/db
      username: root
      password: 123456
  ```
- **修复建议:** 通过环境变量或配置中心注入，使用 `@Value` 或 `@ConfigurationProperties`。
  ```java
  // ✅ 安全：从环境变量/配置中心读取
  @Component
  public class JwtConfig {
      @Value("${jwt.secret}")
      private String secret;
  }
  ```
  ```yaml
  # ✅ 安全：引用环境变量
  spring:
    datasource:
      password: ${DB_PASSWORD}
  ```
- **扣分:** -15
- **误报场景:** 测试用例中的占位密码（如 `password: "test123"`，但应标注 `// test only`）；配置文件中的默认占位值（如 `password: ${DB_PASSWORD:default}`）。

---

### C-SEC-003: 不安全反序列化

- **严重度:** Critical
- **分类:** Security
- **检测模式:** 对不可信来源的数据使用 `ObjectInputStream.readObject()`、`ObjectMapper.enableDefaultTyping()`、Jackson 的 `@JsonTypeInfo` 无白名单、`XStream.fromXML()` 等
- **风险说明:** 未做白名单校验的反序列化可导致远程代码执行（RCE），攻击者通过构造恶意序列化数据触发任意类加载。
- **检测示例:**
  ```java
  // ❌ 危险：无条件反序列化
  public Object deserialize(byte[] data) throws Exception {
      try (ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data))) {
          return ois.readObject();  // 可实例化任意 class
      }
  }
  ```
  ```java
  // ❌ 危险：Jackson 开启默认类型，允许任意类
  ObjectMapper mapper = new ObjectMapper();
  mapper.enableDefaultTyping();  // @Deprecated 且危险
  ```
- **修复建议:** 添加白名单校验，或使用安全的序列化框架。
  ```java
  // ✅ 安全：反序列化前校验 Class
  public Object deserializeSafe(byte[] data) throws Exception {
      try (ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data)) {
          @Override
          protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException {
              String name = desc.getName();
              if (!name.startsWith("com.example.dto.")) {
                  throw new InvalidClassException("Unexpected class", name);
              }
              return super.resolveClass(desc);
          }
      }) {
          return ois.readObject();
      }
  }
  ```
  ```java
  // ✅ 安全：Jackson 显式列出允许的类型
  ObjectMapper mapper = new ObjectMapper();
  mapper.activateDefaultTyping(
      BasicPolymorphicTypeValidator.builder()
          .allowIfSubType("com.example.dto.")
          .build(),
      ObjectMapper.DefaultTyping.NON_FINAL
  );
  ```
- **扣分:** -15
- **误报场景:** 内部系统间通信使用序列化且双方完全受控（如同一个微服务集群内部）。

---

### C-SEC-004: Mass Assignment — `@RequestBody` 无校验

- **严重度:** Critical
- **分类:** Security
- **检测模式:** Controller 中 `@RequestBody` 参数未使用 `@Valid` / `@Validated` 注解，或 DTO 字段未添加校验注解
- **风险说明:** 攻击者可构造请求体包含未预期的字段（如 `role: "ADMIN"`），绕过权限控制直接修改敏感属性。
- **检测示例:**
  ```java
  // ❌ 危险：未校验输入，且 DTO 直接映射数据库
  @PostMapping("/user")
  public User createUser(@RequestBody User user) {
      return userService.save(user);
  }

  // 假设 User 包含 role 字段，攻击者可传 {"name":"hacker","role":"ADMIN"}
  ```
- **修复建议:** 使用 DTO 分离输入输出，添加 `@Valid` 校验。
  ```java
  // ✅ 安全：使用 CreateUserRequest DTO 并添加校验
  @PostMapping("/user")
  public User createUser(@Valid @RequestBody CreateUserRequest request) {
      User user = new User();
      user.setName(request.getName());
      user.setEmail(request.getEmail());
      // role 由业务逻辑赋值，不从请求读取
      user.setRole(Role.USER);
      return userService.save(user);
  }

  // DTO 只包含必要的输入字段
  public class CreateUserRequest {
      @NotBlank
      private String name;

      @Email
      private String email;
  }
  ```
- **扣分:** -15
- **误报场景:** 内部 API 或管理后台 API，调用方完全可信且无敏感字段风险。

---

### C-SEC-005: Open Redirect — 用户可控的 redirect URL

- **严重度:** Critical
- **分类:** Security
- **检测模式:** Controller 方法将请求参数直接拼入 redirect URL，未做白名单校验
- **风险说明:** 攻击者可构造钓鱼链接 `https://yourapp.com/redirect?url=https://malicious.com`，利用用户对可信域名的信任引导至钓鱼页面。
- **检测示例:**
  ```java
  // ❌ 危险：用户可控的重定向
  @GetMapping("/redirect")
  public String redirect(@RequestParam String url) {
      return "redirect:" + url;
  }
  ```
  ```java
  // ❌ 危险：拼接 URL
  @GetMapping("/logout")
  public String logout(HttpServletRequest request) {
      String referer = request.getHeader("Referer");
      return "redirect:" + referer;  // 可通过伪造 Referer 头实现任意跳转
  }
  ```
- **修复建议:** URL 白名单校验或使用固定跳转逻辑。
  ```java
  // ✅ 安全：白名单校验
  private static final Set<String> ALLOWED_DOMAINS = Set.of("example.com", "www.example.com");

  @GetMapping("/redirect")
  public String redirect(@RequestParam String url) {
      try {
          URI uri = new URI(url);
          if (!ALLOWED_DOMAINS.contains(uri.getHost())) {
              return "redirect:/error";
          }
      } catch (URISyntaxException e) {
          return "redirect:/error";
      }
      return "redirect:" + url;
  }
  ```
- **扣分:** -15
- **误报场景:** 所有跳转目标来自硬编码常量或配置文件枚举，未从外部输入获取。

---

### C-REL-001: NPE 风险 — Optional.get() 无检查、返回 null 无 @Nullable

- **严重度:** Critical
- **分类:** Reliability
- **检测模式:** 直接调用 `Optional.get()` 前未做 `isPresent()` 检查；方法返回 `null` 但未标注 `@Nullable`
- **风险说明:** NPE 是 Java 运行时最常见的崩溃原因之一。`Optional.get()` 在无值时报 `NoSuchElementException`；未经标注的 `null` 返回值使调用方无法预判空值风险。
- **检测示例:**
  ```java
  // ❌ 危险：直接 get() 不检查
  public String getUserEmail(Long userId) {
      Optional<User> user = userRepository.findById(userId);
      return user.get().getEmail();  // 如果 userId 不存在则崩溃
  }

  // ❌ 危险：返回 null 无标注
  public String getConfig(String key) {  // 调用者不知道可能返回 null
      return configMap.get(key);
  }
  ```
- **修复建议:** 用 `orElse()` / `orElseThrow()` 替代直接 `get()`；返回值可能为 null 时加 `@Nullable`。
  ```java
  // ✅ 安全：提供默认值或抛出带业务意义的异常
  public String getUserEmail(Long userId) {
      return userRepository.findById(userId)
          .map(User::getEmail)
          .orElseThrow(() -> new UserNotFoundException(userId));
  }

  // ✅ 安全：标注 @Nullable 或使用 Optional 返回
  @Nullable
  public String getConfig(String key) {
      return configMap.get(key);
  }

  // 更好的方式：返回 Optional
  public Optional<String> getConfig(String key) {
      return Optional.ofNullable(configMap.get(key));
  }
  ```
- **扣分:** -15
- **误报场景:** `Optional.get()` 已被 `orElseThrow()` 包裹（不直接调用）；`@Nullable` 已标注但扫描器未识别（如使用了 javax.annotation / checkerframework 等不同包）。

---

### C-REL-002: 资源泄漏 — Stream/Connection 未使用 try-with-resources

- **严重度:** Critical
- **分类:** Reliability
- **检测模式:** `InputStream`、`OutputStream`、`Connection`、`Statement`、`ResultSet`、`Session` 等资源未在 `try-with-resources` 块中关闭
- **风险说明:** 未关闭的资源会导致连接池耗尽、文件句柄泄漏，最终触发 `OutOfMemoryError` 或拒绝服务。即使显式调用 `.close()`，异常路径也可能跳过关闭逻辑。
- **检测示例:**
  ```java
  // ❌ 危险：手动 try-finally 关闭，异常路径遗漏
  public void readFile(String path) throws IOException {
      BufferedReader reader = null;
      try {
          reader = new BufferedReader(new FileReader(path));
          return reader.readLine();
      } finally {
          if (reader != null) reader.close(); // 如果上面抛异常，reader.close() 可能覆盖异常
      }
  }

  // ❌ 危险：Connection 未关闭
  public User findUser(Long id) throws SQLException {
      Connection conn = dataSource.getConnection();
      PreparedStatement ps = conn.prepareStatement("SELECT * FROM user WHERE id = ?");
      ps.setLong(1, id);
      ResultSet rs = ps.executeQuery();
      // 没有任何关闭操作
  }
  ```
- **修复建议:** 使用 `try-with-resources` 自动关闭。
  ```java
  // ✅ 安全：try-with-resources 自动关闭
  public String readFile(String path) throws IOException {
      try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
          return reader.readLine();
      }
  }

  // ✅ 安全：多个资源依次自动关闭
  public User findUser(Long id) throws SQLException {
      String sql = "SELECT * FROM user WHERE id = ?";
      try (Connection conn = dataSource.getConnection();
           PreparedStatement ps = conn.prepareStatement(sql)) {
          ps.setLong(1, id);
          try (ResultSet rs = ps.executeQuery()) {
              if (rs.next()) return mapUser(rs);
              return null;
          }
      }
  }
  ```
- **扣分:** -15
- **误报场景:** Apache DBCP / HikariCP 管理的连接通过连接池返回，`close()` 实际归还而非关闭（但仍应在 finally 中调用 `close()`）；`@Transactional` 管理下 Hibernate Session 由框架管理。

---

### C-REL-003: 事务缺失 — 写操作缺少 `@Transactional`

- **严重度:** Critical
- **分类:** Reliability
- **检测模式:** Service 层方法执行多个写操作（insert/update/delete）但未标注 `@Transactional`
- **风险说明:** 多个数据库写操作不在同一事务中时，中途失败会导致数据不一致（部分写入、部分未写入）。MyBatis Session 默认 auto-commit，每条 SQL 独立提交。
- **检测示例:**
  ```java
  // ❌ 危险：两个写操作不在一事务中
  public class OrderService {
      public void createOrder(Order order) {
          orderMapper.insert(order);          // 第一条 SQL 自动提交成功
          inventoryMapper.reduceStock(order); // 第二条失败，但 order 已经写入！
      }
  }
  ```
- **修复建议:** 添加 `@Transactional`，框架自动管理 begin/commit/rollback。
  ```java
  // ✅ 安全：事务包裹
  @Service
  public class OrderService {
      @Transactional(rollbackFor = Exception.class)
      public void createOrder(Order order) {
          orderMapper.insert(order);
          inventoryMapper.reduceStock(order);
          // 任何一步失败，全部回滚
      }
  }
  ```
- **扣分:** -15
- **误报场景:** 方法内部使用 `TransactionTemplate` 手动管理事务（编程式事务）；方法只涉及一个单表写操作无需事务；只读查询不需要事务（但当查询涉及 N+1 等多次 DB 访问时建议加 `@Transactional(readOnly=true)`）。

---

### C-CFG-001: 生产环境开启 Debug 模式

- **严重度:** Critical
- **分类:** Configuration
- **检测模式:** application.properties/yml 中 `debug: true` 或 `logging.level.root: DEBUG` 在非 dev/test profile 中
- **风险说明:** Debug 日志会打印 SQL 语句、参数详情、堆栈轨迹甚至敏感数据，大幅增加磁盘 I/O 并在外网暴露系统内部细节。
- **检测示例:**
  ```yaml
  # ❌ 危险：application.yml（未按 profile 区分）
  debug: true
  logging:
    level:
      root: DEBUG
  ```
  ```yaml
  # ❌ 危险：application-prod.yml 中仍然 debug
  # application-prod.yml
  debug: true
  jpa:
    show-sql: true
  ```
- **修复建议:** 按 profile 分离配置，生产环境使用 WARN/ERROR 级别。
  ```yaml
  # ✅ 安全：application-dev.yml
  debug: true
  logging:
    level:
      root: DEBUG

  # application-prod.yml
  debug: false
  logging:
    level:
      root: WARN
  ```
- **扣分:** -15
- **误报场景:** 仅存在于 dev/qa 等非生产 profile 中；`logging.level.root=DEBUG` 但通过 `-Dspring.profiles.active=dev` 限制。

---

### C-CFG-002: 非 REST API 缺少 CSRF 保护

- **严重度:** Critical
- **分类:** Configuration
- **检测模式:** 包含基于 Cookie/Session 认证的传统 MVC 应用（非前后端分离）但未配置 CSRF 保护；或未显式禁用 CSRF 的 Spring Security 配置
- **风险说明:** CSRF 攻击可诱导已登录用户执行非本意的写操作（如修改密码、转账）。Spring Security 默认启用 CSRF，但开发者常无意识将其全局禁用。
- **检测示例:**
  ```java
  // ❌ 危险：全局禁用 CSRF 而无替代防护
  @Configuration
  @EnableWebSecurity
  public class SecurityConfig {
      @Bean
      public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
          http
              .csrf(csrf -> csrf.disable())  // 全局关闭 CSRF
              .authorizeHttpRequests(auth -> auth.anyRequest().authenticated());
          return http.build();
      }
  }
  ```
- **修复建议:** 保留 CSRF 保护，或为前后端分离应用显式禁用并使用 Token 认证。
  ```java
  // ✅ 安全：保留 CSRF（或仅对无状态 API 禁用）
  @Configuration
  @EnableWebSecurity
  public class SecurityConfig {
      @Bean
      public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
          http
              // 保留默认 CSRF，或者对纯 API 场景禁用
              .csrf(csrf -> csrf.ignoringRequestMatchers("/api/**"))
              .authorizeHttpRequests(auth -> auth
                  .requestMatchers("/api/**").permitAll()
                  .anyRequest().authenticated()
              );
          return http.build();
      }
  }
  ```
- **扣分:** -15
- **误报场景:** 纯前后端分离应用（REST API + JWT/Token 认证），CSRF 可以安全禁用（无状态服务不需要 CSRF 保护）。

---

### C-CFG-003: Actuator 敏感端点暴露

- **严重度:** Critical
- **分类:** Configuration
- **检测模式:** Spring Boot Actuator 配置中 `/actuator` 未做鉴权，或 `management.endpoints.web.exposure.include=*` 未经安全加固
- **风险说明:** `/actuator/env` 泄露环境变量和密码；`/actuator/beans` 暴露容器配置；`/actuator/actuator/shutdown` 可关闭服务；`/actuator/heapdump` 可下载堆转储（含敏感数据）。
- **检测示例:**
  ```yaml
  # ❌ 危险：暴露所有端点且无鉴权
  management:
    endpoints:
      web:
        exposure:
          include: "*"
  ```
  ```java
  // ❌ 危险：Actuator 端点未集成到 Security 配置中
  ```
- **修复建议:** 仅暴露健康检查端点，并集成 Spring Security 鉴权。
  ```yaml
  # ✅ 安全：只暴露 health 和 info
  management:
    endpoints:
      web:
        exposure:
          include: health,info
    endpoint:
      health:
        show-details: when-authorized  # 不显示详细内容
  ```
  ```java
  // ✅ 安全：Actuator 端点集成鉴权
  @Configuration
  @EnableWebSecurity
  public class SecurityConfig {
      @Bean
      public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
          http
              .requestMatcher(EndpointRequest.toAnyEndpoint())
              .authorizeHttpRequests(auth -> auth.anyRequest().hasRole("ADMIN"));
          return http.build();
      }
  }
  ```
- **扣分:** -15
- **误报场景:** 仅有健康检查端点在内部网络暴露且网络隔离严密；Kubernetes 环境下只通过 Service 暴露特定端口且已做网络策略。

---

## 🟡 Warning Rules

### W-PERF-001: N+1 查询

- **严重度:** Warning
- **分类:** Performance
- **检测模式:** JPA 关联关系（`@OneToMany` / `@ManyToOne` 等）在循环中触发懒加载，导致额外查询
- **风险说明:** 1 条主查询 + N 条关联查询 = N+1。当 N=1000 时，后续 1000 条查询造成显著性能瓶颈，DB 连接池迅速耗尽。
- **检测示例:**
  ```java
  // ❌ 危险：循环内触发懒加载
  public List<OrderDTO> getOrdersByUserIds(List<Long> userIds) {
      List<OrderDTO> result = new ArrayList<>();
      for (Long userId : userIds) {
          User user = userRepository.findById(userId).orElse(null);
          if (user != null) {
              for (Order order : user.getOrders()) {  // 触发 N 次懒加载查询
                  result.add(new OrderDTO(order));
              }
          }
      }
  }
  ```
- **修复建议:** 使用 JOIN FETCH、`@EntityGraph`、或 `@Query` 一次性加载关联。
  ```java
  // ✅ 方案一：JOIN FETCH
  @Query("SELECT u FROM User u JOIN FETCH u.orders WHERE u.id IN :ids")
  List<User> findUsersWithOrders(@Param("ids") List<Long> ids);

  // ✅ 方案二：@EntityGraph
  @EntityGraph(attributePaths = {"orders"})
  List<User> findByIdIn(List<Long> ids);
  ```
- **扣分:** -5
- **误报场景:** 关联实体数量少且固定（如 `status` 枚举表，仅 2-3 条记录）；懒加载是业务预期行为且有关联缓存。

---

### W-PERF-002: 循环中使用字符串拼接

- **严重度:** Warning
- **分类:** Performance
- **检测模式:** for/while 循环中使用 `+` 或 `+=` 拼接字符串
- **风险说明:** `String` 是不可变对象，循环中每次 `+` 都创建新的 `StringBuilder` + 新的 `String` 对象。小 N 影响尚可，但 N>1000 时 GC 压力显著上升。
- **检测示例:**
  ```java
  // ❌ 低效：循环使用 +=
  String result = "";
  for (String item : items) {
      result += item + ",";  // 每次循环创建新对象
  }
  ```
- **修复建议:** 使用 `StringBuilder` 显式构建。
  ```java
  // ✅ 高效：使用 StringBuilder
  StringBuilder sb = new StringBuilder(items.size() * 16);
  for (String item : items) {
      sb.append(item).append(",");
  }
  String result = sb.toString();
  ```
- **扣分:** -5
- **误报场景:** N 很小且固定（如 3-5 个元素且无性能要求）；字符串模板使用 `MessageFormat`/`String.format` 而非 `+`。

---

### W-PERF-003: 不必要地使用自动装箱/拆箱

- **严重度:** Warning
- **分类:** Performance
- **检测模式:** 在循环或频繁调用的方法中使用 `int` ↔ `Integer` / `long` ↔ `Long` 等自动装箱转换
- **风险说明:** 每次装箱创建新对象，循环中大量装箱导致垃圾回收压力和 CPU 开销。
- **检测示例:**
  ```java
  // ❌ 低效：循环中自动装箱
  Integer sum = 0;
  for (int i = 0; i < 1000000; i++) {
      sum += i;  // 每次循环：int→Integer 装箱，然后拆箱做加法，再装箱
  }
  ```
- **修复建议:** 使用基本类型，避免混合类型运算。
  ```java
  // ✅ 高效：使用基本类型
  int sum = 0;
  for (int i = 0; i < 1000000; i++) {
      sum += i;
  }
  ```
- **扣分:** -5
- **误报场景:** `Map<Integer, ...>` 的 Key 操作不可避免装箱；泛型集合需要包装类型。

---

### W-PERF-004: 集合预分配（预知大小时未指定初始容量）

- **严重度:** Warning
- **分类:** Performance
- **检测模式:** `new ArrayList<>()` / `new HashMap<>()` 已知大小但未指定初始容量
- **风险说明:** ArrayList 默认容量 10，超过时自动扩容（50% 增长），每次扩容复制数组。大批量数据场景下扩容次数多，浪费 CPU 和内存。
- **检测示例:**
  ```java
  // ❌ 低效：已知大小但未预分配
  List<User> result = new ArrayList<>();  // 初始 10
  for (User user : userList) {
      result.add(processUser(user));  // 当数据量 >10 时触发多次扩容
  }
  ```
- **修复建议:** 预分配容量，HashMap 还需考虑 load factor。
  ```java
  // ✅ 高效：指定初始容量
  List<User> result = new ArrayList<>(userList.size());

  // HashMap 初始容量 = 预期大小 / load_factor + 1
  Map<String, User> map = new HashMap<>((int) (userList.size() / 0.75) + 1);
  ```
- **扣分:** -5
- **误报场景:** 数据量很小（<10）且固定；实际大小无法预知。

---

### W-DES-001: God Class（上帝类）

- **严重度:** Warning
- **分类:** Design
- **检测模式:** 类代码行数 >500 行或方法数 >20 个
- **风险说明:** 上帝类承担过多职责，违反单一职责原则（SRP）。这类类难以维护、测试、复用和并行开发。
- **检测示例:**
  ```java
  // ❌ 气味：上帝类，超过 500 行
  public class OrderService {
      // 创建订单
      public Order createOrder(...) { ... }
      // 取消订单
      public void cancelOrder(...) { ... }
      // 退款
      public void refund(...) { ... }
      // 发送邮件
      public void sendEmail(...) { ... }
      // 导出报表
      public File exportReport(...) { ... }
      // PDF 生成
      public byte[] generatePdf(...) { ... }
      // ... 20+ 个方法，超过 500 行
  }
  ```
- **修复建议:** 按职责拆分为多个类。
  ```java
  // ✅ 重构：拆分为多个职责单一的类
  @Service
  public class OrderService {
      private final OrderCreationService creationService;
      private final OrderCancelService cancelService;
      private final NotificationService notificationService;
      private final ReportService reportService;
      // 仅做编排
  }

  @Service
  public class OrderCreationService { ... }

  @Service
  public class NotificationService { ... }
  ```
- **扣分:** -5
- **误报场景:** 纯配置类或 `@Configuration` 类（如大量 Bean 定义）；自动生成的代码（如 MyBatis Generator 生成的 Example 类）。

---

### W-DES-002: 长方法（Long Method）

- **严重度:** Warning
- **分类:** Design
- **检测模式:** 单个方法代码 >50 行
- **风险说明:** 长方法难以理解和测试，通常意味着包含多个职责。每个方法应只做一件事。
- **检测示例:**
  ```java
  // ❌ 气味：80 行的方法
  public Order createOrder(CreateOrderRequest request) {
      // 0-20 行：参数校验
      // 20-40 行：库存检查
      // 40-55 行：价格计算
      // 55-65 行：订单持久化
      // 65-80 行：发送通知
  }
  ```
- **修复建议:** 将每个「段落」提取为独立私有方法。
  ```java
  // ✅ 重构：提取子方法
  public Order createOrder(CreateOrderRequest request) {
      validateRequest(request);
      checkInventory(request);
      Order order = new Order();
      calculatePrice(order, request);
      saveOrder(order);
      sendNotification(order);
      return order;
  }

  private void validateRequest(CreateOrderRequest request) { ... }
  private void checkInventory(CreateOrderRequest request) { ... }
  private void calculatePrice(Order order, CreateOrderRequest request) { ... }
  ```
- **扣分:** -5
- **误报场景:** 自动生成的 equals/hashCode/toString；lamda 表达式中的逻辑；switch/case 或 if-else 链条本身较长但逻辑清晰。

---

### W-DES-003: 方法参数过多（>5 个）

- **严重度:** Warning
- **分类:** Design
- **检测模式:** 方法声明中参数数量 >5 个
- **风险说明:** 参数过多导致调用困难、容易传错参数顺序、难以扩展。违反接口隔离原则。
- **检测示例:**
  ```java
  // ❌ 气味：6 个参数，难以阅读
  public void createUser(String name, String email, String phone, String address,
                          String role, Boolean active) { ... }

  // 调用方容易搞混参数顺序
  createUser("张三", "zhang@example.com", "138xxxx", "北京", "admin", true);
  ```
- **修复建议:** 使用参数对象（Parameter Object Pattern）。
  ```java
  // ✅ 重构：封装为参数对象
  public record CreateUserRequest(
      @NotBlank String name,
      @Email String email,
      String phone,
      String address,
      @NotNull UserRole role,
      boolean active
  ) {}

  public void createUser(CreateUserRequest request) { ... }

  // 调用更清晰
  createUser(new CreateUserRequest("张三", "zhang@example.com", ...));
  ```
- **扣分:** -5
- **误报场景:** Spring 注入场景（构造器注入多个依赖）；`@Query` 注解参数（MyBatis 必要时）。

---

### W-DES-004: 循环依赖（Circular Dependency）

- **严重度:** Warning
- **分类:** Design
- **检测模式:** Spring Bean 之间出现 `A → B → A` 或更长的循环引用链
- **风险说明:** 循环依赖导致 Spring 无法完成 Bean 初始化（抛出 `BeanCurrentlyInCreationException`），即使通过 `@Lazy` 或 `setter` 注入勉强运行，也会增加理解和维护成本。
- **检测示例:**
  ```java
  // ❌ 气味：A 依赖 B，B 依赖 A
  @Service
  public class OrderService {
      private final PaymentService paymentService;
      public OrderService(PaymentService paymentService) {
          this.paymentService = paymentService;
      }
  }

  @Service
  public class PaymentService {
      private final OrderService orderService;
      public PaymentService(OrderService orderService) {
          this.orderService = orderService;
      }
  }
  ```
- **修复建议:** 引入中间层或通过事件驱动解耦。
  ```java
  // ✅ 方案一：提取共同依赖到第三个 Service
  @Service
  public class OrderService {
      private final PaymentGateway paymentGateway;  // 不再依赖 PaymentService
  }

  @Service
  public class PaymentService {
      private final OrderRepository orderRepository;  // 使用 Repository 替代 Service
  }

  // ✅ 方案二：使用事件驱动
  @Service
  public class OrderService {
      @Autowired
      private ApplicationEventPublisher eventPublisher;

      public void createOrder(Order order) {
          // ... 保存订单
          eventPublisher.publishEvent(new OrderCreatedEvent(order));
      }
  }

  @Service
  public class PaymentService {
      @EventListener
      public void onOrderCreated(OrderCreatedEvent event) {
          // 异步处理支付，不再依赖 OrderService
      }
  }
  ```
- **扣分:** -5
- **误报场景:** `@Lazy` 有意识地处理（仅限特殊情况且有计划消减）。

---

### W-ERR-001: 异常吞没 — 空 catch 块

- **严重度:** Warning
- **分类:** Error Handling
- **检测模式:** `catch` 块中没有任何处理逻辑（空大括号或仅注释
- **风险说明:** 异常被吞没后完全不可见，导致问题静默失败、排查困难。常出现在「try 一段代码但不知道如何处理异常」的场景。
- **检测示例:**
  ```java
  // ❌ 危险：完全吞没异常
  try {
      userService.createUser(request);
  } catch (Exception e) {
      // do nothing
  }
  ```
- **修复建议:** 至少记录日志；如果确定安全忽略，需明确注释原因。
  ```java
  // ✅ 修复：记录日志
  try {
      userService.createUser(request);
  } catch (Exception e) {
      log.error("创建用户失败, request={}", request, e);
      throw new BusinessException("创建用户失败", e);  // 或转换为业务异常抛出
  }

  // ✅ 或其他：捕获具体异常并处理
  try {
      userService.createUser(request);
  } catch (DuplicateKeyException e) {
      log.warn("用户已存在: {}", request.getEmail());
      return Result.fail("用户已存在");
  }
  ```
- **扣分:** -5
- **误报场景:** `catch` 块中包含 `log.debug()` 或变量赋值（非空，只是扫描器未识别）。

---

### W-ERR-002: 生产代码中使用 `printStackTrace()` / `System.out.println`

- **严重度:** Warning
- **分类:** Error Handling
- **检测模式:** 非测试代码中出现 `e.printStackTrace()`、`System.out.println()`、`System.err.println()`
- **风险说明:** `printStackTrace()` 直接写到 stdout/stderr，在容器化部署中日志难以收集；日志系统中丢失上下文信息，无法按级别过滤和搜索。
- **检测示例:**
  ```java
  // ❌ 不良实践
  try {
      // ...
  } catch (IOException e) {
      e.printStackTrace();  // 写入 stdout，日志采集器可能抓不到
  }

  // ❌ 不良实践：调试输出未清理
  System.out.println("User login: " + userId);
  ```
- **修复建议:** 使用 SLF4J / Logback 等日志框架。
  ```java
  // ✅ 修复：使用日志框架
  private static final Logger log = LoggerFactory.getLogger(UserService.class);

  try {
      // ...
  } catch (IOException e) {
      log.error("文件处理失败, file={}", filePath, e);
  }

  log.info("用户登录: userId={}", userId);
  ```
- **扣分:** -5
- **误报场景:** `main` 方法中的简单演示程序；测试代码（测试框架默认使用 `System.out` 不适用此规则）。

---

### W-ERR-003: 使用过于宽泛的异常捕获

- **严重度:** Warning
- **分类:** Error Handling
- **检测模式:** `catch (Exception e)` 或 `catch (Throwable e)` 捕获非常见顶层异常
- **风险说明:** 捕获所有异常可能隐藏 `NullPointerException`、`IndexOutOfBoundsException` 等编程错误，使调试更困难。`catch (Throwable)` 甚至捕获 `OutOfMemoryError`，掩盖严重系统故障。
- **检测示例:**
  ```java
  // ❌ 危险：捕获所有异常
  try {
      processOrder(order);
  } catch (Exception e) {
      log.error("处理失败", e);
  }
  ```
- **修复建议:** 捕获具体异常类型。
  ```java
  // ✅ 修复：捕获具体异常
  try {
      processOrder(order);
  } catch (OrderNotFoundException e) {
      log.warn("订单不存在: {}", order.getId());
      return Result.fail("订单不存在");
  } catch (InsufficientStockException e) {
      log.warn("库存不足: {}", e.getMessage());
      return Result.fail("库存不足");
  } catch (Exception e) {
      // 最后一个兜底 catch 可以保留，但需确认业务场景合理
      log.error("处理订单未知异常, orderId={}", order.getId(), e);
      throw new BusinessException("系统繁忙", e);
  }
  ```
- **扣分:** -5
- **误报场景:** Spring 的全局异常处理器（`@ControllerAdvice`）中的 `catch (Exception e)` 作为兜底；框架级别的 `Filter` 或 `Interceptor` 中需要保证不抛出异常的场景。

---

### W-ERR-004: 方法抛出过于宽泛的异常

- **严重度:** Warning
- **分类:** Error Handling
- **检测模式:** 方法签名中使用 `throws Exception` / `throws Throwable` 而非具体异常
- **风险说明:** 宽泛异常使调用方无法区分异常原因，被迫吞没或同样向上抛出宽泛异常，形成「异常模糊化」的恶性链条。
- **检测示例:**
  ```java
  // ❌ 不良实践
  public void importData(MultipartFile file) throws Exception {
      // 不知道会有什么异常
  }

  // 调用方只能：
  try {
      importData(file);
  } catch (Exception e) {
      // 不知道具体是什么异常，无法精细化处理
  }
  ```
- **修复建议:** 声明具体业务或系统异常。
  ```java
  // ✅ 修复：声明具体异常
  public void importData(MultipartFile file) throws IOException, DataValidationException {
      if (file.isEmpty()) throw new DataValidationException("文件不能为空");
      List<String> lines = Files.readAllLines(Paths.get(file.getOriginalFilename()));
      // ...
  }

  // 调用方可以：
  try {
      importData(file);
  } catch (IOException e) {
      log.error("文件读取失败", e);
  } catch (DataValidationException e) {
      log.warn("数据校验失败: {}", e.getMessage());
      return Result.fail(e.getMessage());
  }
  ```
- **扣分:** -5
- **误报场景:** 接口/抽象方法定义；Spring AOP 代理方法（某些框架限制要求抛出 `Throwable`）；`Callable<V>` 或 `Runnable` 等函数式接口。

---

### W-TST-001: 测试方法缺少断言

- **严重度:** Warning
- **分类:** Testing
- **检测模式:** 使用 `@Test` 标注的方法但没有 `assert*` 调用
- **风险说明:** 没有断言的测试不验证任何结果，即使逻辑完全执行错也「通过」——这种假阳性的测试比没有测试更危险。
- **检测示例:**
  ```java
  // ❌ 无意义：没有断言的测试
  @Test
  public void testCreateUser() {
      User user = new User("test@example.com");
      userService.createUser(user);
      // 没有验证结果，任何执行都算通过
  }
  ```
- **修复建议:** 添加返回值验证或状态检测。
  ```java
  // ✅ 有效：添加断言
  @Test
  public void testCreateUser() {
      User user = new User("test@example.com");
      userService.createUser(user);

      User saved = userRepository.findByEmail("test@example.com");
      assertThat(saved).isNotNull();
      assertThat(saved.getEmail()).isEqualTo("test@example.com");
      assertThat(saved.getCreatedAt()).isNotNull();
  }
  ```
- **扣分:** -5
- **误报场景:** 测试方法中调用了其他包含断言的辅助方法；`@Test(expected = ...)` 形式（异常本身就是一种断言）；使用 Mockito `verify()` 替代 assert（应检查 verify 是否存在）。

---

### W-TST-002: 测试中使用 `Thread.sleep()`

- **严重度:** Warning
- **分类:** Testing
- **检测模式:** 测试代码中出现 `Thread.sleep()`
- **风险说明:** 测试中使用 `sleep` 等待异步结果，会产生不稳定（flaky）测试：CI 环境负载高时 sleep 时间不够导致偶然失败，或 sleep 时间过长浪费 CI 资源。
- **检测示例:**
  ```java
  // ❌ 不可靠：使用 Thread.sleep
  @Test
  public void testAsyncEmailSending() throws Exception {
      emailService.sendAsync(email);
      Thread.sleep(3000);  // 不确定的等待，本地 OK，CI 可能失败
      assertThat(emailService.getSentCount()).isEqualTo(1);
  }
  ```
- **修复建议:** 使用 Awaitility 框架轮询等待条件。
  ```java
  // ✅ 可靠：使用 Awaitility
  @Test
  public void testAsyncEmailSending() {
      emailService.sendAsync(email);

      await().atMost(5, TimeUnit.SECONDS)
             .pollInterval(100, TimeUnit.MILLISECONDS)
             .untilAsserted(() -> {
                 assertThat(emailService.getSentCount()).isEqualTo(1);
             });
  }
  ```
- **扣分:** -5
- **误报场景:** 测试特定定时器场景且时间极短（如 `Thread.sleep(10)` 等待时间片切换）；集成测试中等待外部系统（如第三方 API 回调，但应优先 mock）。

---

## 🟢 Info Rules

### I-CON-001: 命名规范违规

- **严重度:** Info
- **分类:** Convention
- **检测模式:** 类名非帕斯卡命名（PascalCase）、方法名非驼峰命名（camelCase）、常量名非全大写带下划线（UPPER_SNAKE_CASE）、包名非全小写
- **风险说明:** 违反 Java 社区通用命名规范降低代码可读性，使新成员加入时易产生困惑。
- **检测示例:**
  ```java
  // ❌ 不规范
  public class order_service { ... }                 // 类名应 PascalCase
  public void Find_User() { ... }                    // 方法名应 camelCase
  public static final int max_retry_count = 3;       // 常量应 UPPER_SNAKE_CASE
  package Com.Example.Utils;                         // 包名应全小写
  ```
- **修复建议:** 按 Java 命名约定重构。
  ```java
  // ✅ 规范
  public class OrderService { ... }
  public void findUser() { ... }
  public static final int MAX_RETRY_COUNT = 3;
  package com.example.utils;
  ```
- **扣分:** -1
- **误报场景:** 与框架约定的特殊命名（如 Spring 的 `application.properties`、`logback-spring.xml`）；自动生成的类（MyBatis Generator 生成的 Example 类）。

---

### I-CON-002: 包结构不符合标准分层

- **严重度:** Info
- **分类:** Convention
- **检测模式:** 未遵循 Spring Boot 推荐的分层结构（controller / service / repository / dto / config / util 等），或大量类堆在同一个包下
- **风险说明:** 缺乏清晰的分层结构使项目导航困难，职责边界模糊，容易产生循环依赖。
- **检测示例:**
  ```text
  // ❌ 混乱的包结构
  src/main/java/com/example/
    ├── Order.java          // entity? service? 不明确
    ├── OrderController.java
    ├── OrderServiceImpl.java
    ├── UserHelper.java
    ├── MainConfig.java
    └── OrderStuff.java
  ```
- **修复建议:** 按功能 + 层结构组织。
  ```text
  // ✅ 推荐的包结构
  src/main/java/com/example/
    ├── controller/
    │   ├── OrderController.java
    │   └── UserController.java
    ├── service/
    │   ├── OrderService.java
    │   └── impl/
    │       └── OrderServiceImpl.java
    ├── repository/
    │   ├── OrderRepository.java
    │   └── UserRepository.java
    ├── entity/
    │   ├── Order.java
    │   └── User.java
    ├── dto/
    │   ├── CreateOrderRequest.java
    │   └── OrderResponse.java
    ├── config/
    │   ├── SecurityConfig.java
    │   └── SwaggerConfig.java
    └── common/
        ├── Result.java
        └── GlobalExceptionHandler.java
  ```
- **扣分:** -1
- **误报场景:** 小型项目（<10 个文件）不需要严格分层；模块化项目使用 `module/controller` 等替代单一分层。

---

### I-CON-003: 技术债务注释过多 — TODO/FIXME/HACK

- **严重度:** Info
- **分类:** Convention
- **检测模式:** 项目中 TODO / FIXME / HACK / XXX 注释数量超过阈值（默认 5 个）
- **风险说明:** 堆积的 TODO 代表未完成的改进、已知缺陷或临时方案，长期无人跟进会逐渐变成不可处理的僵尸代码。
- **检测示例:**
  ```java
  // ❌ 多个残留 TODO
  // TODO: 需要处理超时
  // TODO: 添加事务
  // FIXME: 性能问题，需要优化
  // HACK: 临时修复，等对方修复后删除
  // TODO: 补充单元测试
  ```
- **修复建议:** 审查后清理：确实要做的创建 Issue/Ticket，不紧急的删除。留下 TODO 至少标注责任人和日期。
  ```java
  // ✅ 规范的 TODO
  // TODO(@zhangsan, 2026-05-18): 添加超时重试机制，详情见 ISSUE-1234
  if (retryCount < 3) { ... }
  ```
- **扣分:** -1（按每个超过阈值的计数）
- **误报场景:** 代码生成器自动生成的注释；IDE 自动添加的标准 `// TODO` 模板但已有对应任务追踪。

---

### I-CON-004: 缺少 Javadoc 注释

- **严重度:** Info
- **分类:** Convention
- **检测模式:** public API（类、方法、字段）缺少 Javadoc 注释
- **风险说明:** 缺少文档的 public API 使调用方需要阅读源码才能了解行为，降低可维护性和协作效率。
- **检测示例:**
  ```java
  // ❌ 缺少文档
  public class OrderService {
      /**
       * 根据用户 ID 查询订单
       */
      public PageResult findOrders(Long userId, Pageable pageable, OrderStatus status) {
          // ...
      }
  }
  ```
- **修复建议:** 为 public API 添加 Javadoc，说明功能、参数和返回值。
  ```java
  // ✅ 良好的 Javadoc
  /**
   * 根据用户 ID 分页查询订单，支持按状态过滤。
   *
   * @param userId  用户 ID（必填）
   * @param pageable 分页参数（含排序）
   * @param status   订单状态过滤，为 null 时查询所有状态
   * @return 分页结果，含当前页数据和总记录数
   * @throws IllegalArgumentException userId 为 null 时抛出
   */
  public PageResult findOrders(@NotNull Long userId, @NotNull Pageable pageable,
                                @Nullable OrderStatus status) {
      // ...
  }
  ```
- **扣分:** -1（按缺失比例扣分，>50% public API 缺 Javadoc 时扣 3 分）
- **误报场景:** Getter/Setter/toString/equals/hashCode；被 `@Deprecated` 标注并注明替代方案；Spring Controller 方法使用 Swagger 注解（`@ApiOperation`、`@ApiParam`）替代。

---

### I-DEP-001: 依赖版本滞后

- **严重度:** Info
- **分类:** Dependencies
- **检测模式:** pom.xml / build.gradle 中声明的依赖版本落后于最新稳定版本超过 2 个大版本
- **风险说明:** 依赖版本严重滞后意味着缺失安全补丁和性能优化，且从老版本大跨度升级的迁移成本较高。Spring Boot 3.x 到 Spring Boot 4.x 的大版本变化尤其需要注意。
- **检测示例:**
  ```xml
  <!-- ❌ 落后：Spring Boot 2.3.x vs 最新 3.x -->
  <parent>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>2.7.18</version>  <!-- 落后 2.7.x 是早期 3.x 前的过渡版本 -->
  </parent>
  ```
  ```xml
  <!-- ❌ 落后：Guava 30.x vs 最新 33.x -->
  <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>30.0-jre</version>  <!-- 落后 3 个大版本 -->
  </dependency>
  ```
- **修复建议:** 定期检查和升级依赖版本。

  ```xml
  <!-- ✅ 更新到最新大版本（需测试兼容性） -->
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>3.4.0</version>
  </dependency>
  ```
- **扣分:** -1
- **误报场景:** 特定版本有兼容性问题，故意锁定在老版本且有注释说明原因；内部私有依赖无法升级；`pom.xml` 中的 `properties` 版本变量而非硬编码版本（需解析实际值）。

---

### I-DEP-002: 声明但未使用的依赖

- **严重度:** Info
- **分类:** Dependencies
- **检测模式:** `pom.xml` / `build.gradle` 中声明的依赖未在源码中引用
- **风险说明:** 未使用的依赖增加构建时间、包体积和攻击面；冗余的传递依赖可能导致意外冲突。
- **检测示例:**
  ```xml
  <!-- ❌ 未使用：项目中从未 import commons-lang3 -->
  <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
      <version>3.14.0</version>
  </dependency>
  ```
- **修复建议:** 使用 Maven `dependency:analyze` 发现并移除未使用依赖。
  ```bash
  mvn dependency:analyze
  ```
- **扣分:** -1
- **误报场景:** 通过反射、SPI 或 ClassLoader 动态加载的依赖（Maven analyzer 可能误报）；编译期注解处理器如 Lombok、MapStruct；`test` scope 但也有同样问题（测试代码未使用）。

---

### I-DEP-003: 生产构建使用 SNAPSHOT 版本

- **严重度:** Info
- **分类:** Dependencies
- **检测模式:** `pom.xml` 中声明的依赖版本包含 `-SNAPSHOT` 后缀
- **风险说明:** SNAPSHOT 版本表示不稳定、可能随时变更的构建。生产环境使用 SNAPSHOT 依赖意味着每次构建结果可能不同，无法复现构建。
- **检测示例:**
  ```xml
  <!-- ❌ 不推荐：生产使用 SNAPSHOT -->
  <dependency>
      <groupId>com.example</groupId>
      <artifactId>internal-sdk</artifactId>
      <version>1.2.3-SNAPSHOT</version>
  </dependency>
  ```
- **修复建议:** 使用正式 release 版本，或定期发布正式版本供生产使用。
  ```xml
  <!-- ✅ 修复：使用 release 版本 -->
  <dependency>
      <groupId>com.example</groupId>
      <artifactId>internal-sdk</artifactId>
      <version>1.3.0</version>
  </dependency>
  ```
- **扣分:** -1
- **误报场景:** 仅在 dev profile 中使用的 SNAPSHOT 依赖；项目自身是开发库且处于开发阶段（但生产部署时应锁定 version）。

---

### I-DEP-004: 传递依赖版本冲突

- **严重度:** Info
- **分类:** Dependencies
- **检测模式:** 多个依赖引入了同一传递依赖的不同版本，Maven 按「最短路径优先」选择了较低或错误版本
- **风险说明:** 版本冲突可能导致 `NoSuchMethodError`、`ClassNotFoundException` 等运行时错误。常发生在引入多个大型框架（如 Spring + Hibernate + Apache Camel）时。
- **检测示例:**
  ```text
  // ❌ 冲突示例：
  // jackson-core 2.15.0 (直接依赖 A)
  // jackson-core 2.13.0 (传递依赖 B → C → jackson-core 2.13.0)
  // Maven 选择 2.13.0（路径更短），但 A 需要使用 2.15.0 的新 API
  ```
- **修复建议:** 使用 `<dependencyManagement>` 统一版本管理，或通过 `mvn dependency:tree` 分析并显式声明冲突版本。
  ```xml
  <!-- ✅ 修复：在 dependencyManagement 中统一版本 -->
  <dependencyManagement>
      <dependencies>
          <dependency>
              <groupId>com.fasterxml.jackson.core</groupId>
              <artifactId>jackson-core</artifactId>
              <version>2.16.0</version>
          </dependency>
      </dependencies>
  </dependencyManagement>
  ```
  ```bash
  # 分析依赖树
  mvn dependency:tree -Dverbose
  ```
- **扣分:** -1
- **误报场景:** 使用 Maven BOM（Bill of Materials）已统一管理版本；Spring Boot Parent POM 已经通过 `spring-boot-dependencies` 处理了兼容版本。

---

## 附录：评分扣分表

| 严重度 | 单次扣分 | 上限 |
|--------|---------|------|
| 🔴 Critical | -15 | 无（但总分下限 0） |
| 🟡 Warning | -5 | 无（但总分下限 0） |
| 🟢 Info | -1 | -10（避免 Info 级问题过度影响分数） |

### 评分公式

```
Health Score = max(0, 100 - (Critical_Count × 15) - (Warning_Count × 5) - min(Info_Count, 10))
```

### 健康等级

| 分数范围 | 标签 | 含义 |
|---------|------|------|
| ≥ 85 | ✅ Healthy | 代码质量良好 |
| 70–84 | 🟡 Needs Attention | 有一些需关注的问题 |
| < 70 | 🔴 At Risk | 存在严重风险，建议优先修复 |

### 各规则 ID 速查表

| ID | Severity | Category | Rule |
|----|----------|----------|------|
| C-SEC-001 | 🔴 Critical | Security | SQL 注入 — MyBatis `${}` |
| C-SEC-002 | 🔴 Critical | Security | 硬编码密钥/密码 |
| C-SEC-003 | 🔴 Critical | Security | 不安全反序列化 |
| C-SEC-004 | 🔴 Critical | Security | Mass Assignment（无校验 `@RequestBody`） |
| C-SEC-005 | 🔴 Critical | Security | Open Redirect |
| C-REL-001 | 🔴 Critical | Reliability | NPE 风险 |
| C-REL-002 | 🔴 Critical | Reliability | 资源泄漏 |
| C-REL-003 | 🔴 Critical | Reliability | 事务缺失 |
| C-CFG-001 | 🔴 Critical | Configuration | 生产环境 Debug 模式 |
| C-CFG-002 | 🔴 Critical | Configuration | 缺少 CSRF 保护 |
| C-CFG-003 | 🔴 Critical | Configuration | Actuator 敏感端点暴露 |
| W-PERF-001 | 🟡 Warning | Performance | N+1 查询 |
| W-PERF-002 | 🟡 Warning | Performance | 循环字符串拼接 |
| W-PERF-003 | 🟡 Warning | Performance | 自动装箱/拆箱 |
| W-PERF-004 | 🟡 Warning | Performance | 集合未预分配容量 |
| W-DES-001 | 🟡 Warning | Design | God Class（上帝类） |
| W-DES-002 | 🟡 Warning | Design | 长方法 |
| W-DES-003 | 🟡 Warning | Design | 参数过多 |
| W-DES-004 | 🟡 Warning | Design | 循环依赖 |
| W-ERR-001 | 🟡 Warning | Error Handling | 异常吞没（空 catch） |
| W-ERR-002 | 🟡 Warning | Error Handling | printStackTrace / System.out |
| W-ERR-003 | 🟡 Warning | Error Handling | 宽泛异常捕获 |
| W-ERR-004 | 🟡 Warning | Error Handling | 抛出宽泛异常 |
| W-TST-001 | 🟡 Warning | Testing | 测试缺少断言 |
| W-TST-002 | 🟡 Warning | Testing | 测试中使用 Thread.sleep |
| I-CON-001 | 🟢 Info | Convention | 命名规范 |
| I-CON-002 | 🟢 Info | Convention | 包结构规范 |
| I-CON-003 | 🟢 Info | Convention | TODO/FIXME 堆积 |
| I-CON-004 | 🟢 Info | Convention | 缺少 Javadoc |
| I-DEP-001 | 🟢 Info | Dependencies | 依赖版本滞后 |
| I-DEP-002 | 🟢 Info | Dependencies | 未使用的依赖 |
| I-DEP-003 | 🟢 Info | Dependencies | 生产使用 SNAPSHOT |
| I-DEP-004 | 🟢 Info | Dependencies | 传递依赖版本冲突 |

---

> **文档版本:** v1.0  
> **最后更新:** 2026-05-18  
> **规则总数:** 11 🔴 + 14 🟡 + 8 🟢 = **33 条规则**
