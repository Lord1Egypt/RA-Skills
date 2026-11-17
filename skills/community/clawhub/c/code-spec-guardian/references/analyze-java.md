# Java 规范分析指引 | Java Analyzer

> 覆盖 Java 项目的语言特有规范。以项目实际配置为准。

## 分析流程

1. 读 `references/analyze-code-style.md` 中的通用部分
2. 用 `read` 读 `pom.xml` / `build.gradle` / `application.yml`（或从 `project_context.json` → `configs` 中获取片段）
3. 追加写入 `.code-spec/java-style.md`（Java 特有条目，不要写入 code-style.md）

## Java 特有分析维度

### 命名

- **类**：PascalCase
- **方法/变量**：camelCase
- **常量**：UPPER_SNAKE_CASE
- **包**：全小写，域名倒序（com.company.project）
- **接口**：是否有 I 前缀（IPrefix）还是 Impl 后缀
- **DTO/VO/BO/PO/DO**：命名约定和包位置
- **Enum**：枚举值是否全大写

### 包结构

- 分层模式：controller → service → service.impl → mapper/repository → entity/model
- 领域模式：domain → application → infrastructure
- 各层接口和实现的分离程度
- common/util/config 目录的组织

### 注解使用

- **Lombok**：`@Data` / `@Getter` / `@Setter` / `@Builder` / `@Slf4j` / `@AllArgsConstructor` 使用约定
- **Spring**：`@RestController` / `@Service` / `@Repository` / `@Component` / `@Autowired` vs 构造注入
- **校验**：`@Valid` / `@Validated` / `@NotNull` / `@NotBlank` 等 javax.validation 使用
- **文档**：Swagger/OpenAPI 注解 `@ApiOperation` / `@ApiModelProperty`
- **Mapping**：`@RequestMapping` / `@GetMapping` / `@PostMapping` 风格

### 代码风格

- **缩进**：4 空格 vs Tab
- **大括号**：埃及括号（Egyptian braces）还是次行
- **行长**：120 / 150 字符
- **import**：禁止 `*` 导入，全限定导入
- **final** 使用：方法参数是否加 final
- **日志**：`@Slf4j` 还是 `LoggerFactory.getLogger()`，日志级别使用
- **注释**：Javadoc 在所有公共方法上？`@param` / `@return` / `@throws`

### Spring 配置

- `application.yml` vs `application.properties`
- Profile 管理（dev / test / prod）
- `@Configuration` 类组织
- `@Value` vs `@ConfigurationProperties` 使用
- 配置中心（Nacos / Apollo / Consul）
- 多模块项目的模块划分

### 依赖注入与 Bean

- 构造注入 vs `@Autowired` 字段注入 vs setter 注入
- `@Primary` / `@Qualifier` 处理多实现

### 错误处理

- 全局异常处理：`@ControllerAdvice` / `@RestControllerAdvice`
- 业务异常体系：自定义 RuntimeException 子类，错误码枚举
- `try-catch` 粒度

### 数据层

- **MyBatis**：XML mapper vs 注解 SQL，mapper 位置约定
- **MyBatis-Plus**：BaseMapper / IService 使用，条件构造器风格
- **JPA/Hibernate**：Entity 定义，Repository 接口
- **Redis**：序列化方式、key 命名、Template 使用

### 测试

- JUnit 4 vs JUnit 5
- Mockito 使用
- `src/test/java` 目录结构与主代码镜像
- 集成测试 vs 单元测试分离

### 构建

- Maven vs Gradle
- 多模块依赖管理
- 版本号管理（parent pom / BOM / version catalog）
- profile 管理

### 工具链

- Checkstyle 配置
- SpotBugs / SonarQube
- 代码格式化：Eclipse formatter / Google Java Format
