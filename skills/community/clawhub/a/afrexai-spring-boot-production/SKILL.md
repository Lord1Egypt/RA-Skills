# Spring Boot Production Engineering

> Complete production engineering methodology for Spring Boot & Java/Kotlin applications — architecture, security, observability, testing, deployment, and performance optimization.

## Quick Health Check

Score your Spring Boot application (1 = needs work, 2 = acceptable):

| Signal | Check | /2 |
|--------|-------|----|
| 🏗️ Architecture | Clean layered architecture with dependency injection? | |
| 🔒 Security | Spring Security configured with proper auth + CORS + CSRF? | |
| 📊 Observability | Structured logging + metrics + health endpoints? | |
| 🧪 Testing | Unit + integration + slice tests with >70% coverage? | |
| ⚡ Performance | Connection pooling + caching + async where appropriate? | |
| 🚀 Deployment | Containerized with CI/CD + zero-downtime deploys? | |
| 📝 API Design | OpenAPI docs + versioning + consistent error responses? | |
| 🛡️ Resilience | Circuit breakers + retries + graceful degradation? | |

**Score: /16** → ≤8 Critical · 9-12 Improving · 13-14 Good · 15-16 Production-ready

---

## Phase 1: Project Architecture

### Recommended Project Structure

```
src/main/java/com/example/app/
├── Application.java                 # @SpringBootApplication entry
├── config/                          # Configuration classes
│   ├── SecurityConfig.java
│   ├── WebConfig.java
│   ├── CacheConfig.java
│   └── AsyncConfig.java
├── domain/                          # Domain models & business logic
│   ├── model/                       # JPA entities / domain objects
│   ├── repository/                  # Spring Data repositories
│   ├── service/                     # Business logic services
│   └── event/                       # Domain events
├── api/                             # REST controllers
│   ├── controller/                  # @RestController classes
│   ├── dto/                         # Request/Response DTOs
│   ├── mapper/                      # Entity ↔ DTO mappers
│   └── exception/                   # API exception handlers
├── infrastructure/                  # External integrations
│   ├── client/                      # REST/gRPC clients
│   ├── messaging/                   # Kafka/RabbitMQ producers/consumers
│   └── storage/                     # S3/file storage
└── common/                          # Shared utilities
    ├── exception/                   # Base exceptions
    ├── validation/                  # Custom validators
    └── util/                        # Helpers
```

### 7 Architecture Rules

1. **Controllers are thin** — validate input, call service, return DTO. No business logic.
2. **Services own business logic** — transaction boundaries live here.
3. **Repositories are interfaces** — Spring Data generates implementations.
4. **DTOs at boundaries** — never expose JPA entities in API responses.
5. **Constructor injection only** — no `@Autowired` on fields (testability).
6. **Package by feature for large apps** — when >20 services, switch from layer-based to feature-based.
7. **No circular dependencies** — if A depends on B depends on A, extract shared logic to C.

### Spring Boot Starter Selection

```yaml
# build.gradle.kts (recommended over Maven for Kotlin DSL + type safety)
dependencies:
  # Core
  - spring-boot-starter-web          # REST APIs (embedded Tomcat)
  - spring-boot-starter-webflux      # Reactive APIs (Netty) — choose ONE
  - spring-boot-starter-validation   # Bean Validation (Jakarta)
  
  # Data
  - spring-boot-starter-data-jpa     # JPA + Hibernate
  - spring-boot-starter-data-redis   # Redis caching
  
  # Security
  - spring-boot-starter-security     # Spring Security
  - spring-boot-starter-oauth2-resource-server  # JWT validation
  
  # Observability
  - spring-boot-starter-actuator     # Health, metrics, info
  - micrometer-registry-prometheus   # Prometheus metrics export
  
  # Resilience
  - resilience4j-spring-boot3        # Circuit breaker, retry, rate limit
  
  # Testing
  - spring-boot-starter-test         # JUnit 5 + Mockito + AssertJ
  - spring-boot-testcontainers       # Real DB/Redis in tests
```

### Framework Decision: Spring Boot vs Alternatives

| Factor | Spring Boot | Quarkus | Micronaut | Ktor (Kotlin) |
|--------|------------|---------|-----------|---------------|
| Startup time | 2-5s | 0.5-1s | 1-2s | 1-2s |
| Memory | 200-400MB | 50-150MB | 100-200MB | 80-150MB |
| Ecosystem | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ |
| Enterprise adoption | Dominant | Growing | Niche | Niche |
| Native compilation | GraalVM (complex) | Native (easy) | Native (easy) | GraalVM |
| Team hiring | Easy | Hard | Hard | Hard |

**Decision rule**: Spring Boot unless startup time <1s is critical (serverless/CLI) → Quarkus.

---

## Phase 2: Configuration & Profiles

### application.yml Production Template

```yaml
spring:
  application:
    name: ${APP_NAME:my-service}
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:local}
  
  # Database
  datasource:
    url: ${DATABASE_URL:jdbc:postgresql://localhost:5432/mydb}
    username: ${DATABASE_USERNAME:postgres}
    password: ${DATABASE_PASSWORD:postgres}
    hikari:
      maximum-pool-size: ${DB_POOL_SIZE:10}
      minimum-idle: ${DB_POOL_MIN:5}
      connection-timeout: 3000
      idle-timeout: 600000
      max-lifetime: 1800000
      leak-detection-threshold: 60000
  
  jpa:
    open-in-view: false  # CRITICAL — disable OSIV anti-pattern
    hibernate:
      ddl-auto: validate  # Production: NEVER use update/create
    properties:
      hibernate:
        default_batch_fetch_size: 25
        order_inserts: true
        order_updates: true
        jdbc:
          batch_size: 50
          batch_versioned_data: true
  
  # Jackson
  jackson:
    default-property-inclusion: non_null
    serialization:
      write-dates-as-timestamps: false
    deserialization:
      fail-on-unknown-properties: false
  
  # Cache
  cache:
    type: redis
    redis:
      time-to-live: 3600000  # 1 hour default

server:
  port: ${SERVER_PORT:8080}
  shutdown: graceful  # Wait for active requests
  tomcat:
    max-threads: ${TOMCAT_MAX_THREADS:200}
    accept-count: 100
    connection-timeout: 5000

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true  # Kubernetes liveness/readiness
  metrics:
    tags:
      application: ${spring.application.name}

# Graceful shutdown
spring.lifecycle.timeout-per-shutdown-phase: 30s
```

### Profile Strategy

| Profile | Purpose | Config |
|---------|---------|--------|
| `local` | Development | H2/local Postgres, debug logging |
| `test` | Testing | Testcontainers, no external deps |
| `staging` | Pre-production | Real deps, reduced resources |
| `production` | Live | Full resources, minimal logging |

### Configuration Rules

1. **Never hardcode secrets** — always use environment variables or vault
2. **Disable `open-in-view`** — prevents lazy loading in controller layer (performance killer)
3. **Set `ddl-auto: validate`** in production — use Flyway/Liquibase for migrations
4. **Configure HikariCP explicitly** — defaults are often wrong for production
5. **Enable graceful shutdown** — `server.shutdown: graceful` + timeout

---

## Phase 3: JPA & Database Patterns

### Entity Design

```java
@MappedSuperclass
public abstract class BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @CreationTimestamp
    @Column(updatable = false)
    private Instant createdAt;
    
    @UpdateTimestamp
    private Instant updatedAt;
    
    @Version  // Optimistic locking
    private Long version;
}

@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_users_email", columnList = "email", unique = true),
    @Index(name = "idx_users_status", columnList = "status")
})
public class User extends BaseEntity {
    
    @Column(nullable = false, length = 255)
    private String email;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private UserStatus status;
    
    @OneToMany(mappedBy = "user", fetch = FetchType.LAZY)  // ALWAYS lazy
    private List<Order> orders = new ArrayList<>();
}
```

### N+1 Prevention

```java
// ❌ N+1 problem — loads each user's orders individually
List<User> users = userRepository.findAll();
users.forEach(u -> u.getOrders().size());  // N additional queries

// ✅ JOIN FETCH — single query
@Query("SELECT u FROM User u JOIN FETCH u.orders WHERE u.status = :status")
List<User> findByStatusWithOrders(@Param("status") UserStatus status);

// ✅ EntityGraph — declarative
@EntityGraph(attributePaths = {"orders", "orders.items"})
List<User> findByStatus(UserStatus status);

// ✅ Batch fetching (configured globally)
# application.yml: hibernate.default_batch_fetch_size: 25
```

### Repository Patterns

```java
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Derived queries — simple cases only
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    
    // Projections — return only needed fields
    @Query("SELECT new com.example.dto.UserSummary(u.id, u.email, u.status) " +
           "FROM User u WHERE u.status = :status")
    List<UserSummary> findSummariesByStatus(@Param("status") UserStatus status);
    
    // Pagination
    Page<User> findByStatus(UserStatus status, Pageable pageable);
    
    // Bulk operations — bypass Hibernate cache
    @Modifying(clearAutomatically = true)
    @Query("UPDATE User u SET u.status = :status WHERE u.lastLoginAt < :threshold")
    int deactivateInactiveUsers(@Param("status") UserStatus status,
                                @Param("threshold") Instant threshold);
}
```

### Migration with Flyway

```sql
-- V1__create_users_table.sql
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    email       VARCHAR(255) NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version     BIGINT NOT NULL DEFAULT 0,
    CONSTRAINT uk_users_email UNIQUE (email)
);

CREATE INDEX idx_users_status ON users(status);
```

### 8 JPA Rules

1. **Always use `FetchType.LAZY`** — eager loading causes N+1
2. **Use `@Version` for optimistic locking** — prevents lost updates
3. **Prefer projections over full entities** — `SELECT new DTO(...)` for read-only
4. **Batch inserts/updates** — configure `batch_size` + `order_inserts`
5. **Never use `ddl-auto: update` in production** — Flyway/Liquibase only
6. **Use `@NaturalId` for business keys** — email, ISBN, etc.
7. **Avoid bidirectional mappings unless needed** — more complexity, more bugs
8. **Test queries with real database** — Testcontainers, not H2

---

## Phase 4: REST API Design

### Controller Pattern

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
public class UserController {
    
    private final UserService userService;
    private final UserMapper userMapper;
    
    @GetMapping
    public Page<UserResponse> listUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) UserStatus status) {
        
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        return userService.findUsers(status, pageable)
                .map(userMapper::toResponse);
    }
    
    @GetMapping("/{id}")
    public UserResponse getUser(@PathVariable Long id) {
        return userMapper.toResponse(userService.findById(id));
    }
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        User user = userService.create(request);
        return userMapper.toResponse(user);
    }
    
    @PutMapping("/{id}")
    public UserResponse updateUser(@PathVariable Long id,
                                    @Valid @RequestBody UpdateUserRequest request) {
        User user = userService.update(id, request);
        return userMapper.toResponse(user);
    }
    
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

### DTO Validation

```java
public record CreateUserRequest(
    @NotBlank @Email @Size(max = 255)
    String email,
    
    @NotBlank @Size(min = 2, max = 100)
    String name,
    
    @NotNull
    UserRole role
) {}

public record UserResponse(
    Long id,
    String email,
    String name,
    UserStatus status,
    Instant createdAt
) {}
```

### Global Error Handling

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    
    @ExceptionHandler(EntityNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(EntityNotFoundException ex) {
        return new ErrorResponse("NOT_FOUND", ex.getMessage());
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = ex.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                fe -> fe.getDefaultMessage() != null ? fe.getDefaultMessage() : "invalid",
                (a, b) -> a
            ));
        return new ErrorResponse("VALIDATION_ERROR", "Invalid request", errors);
    }
    
    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ErrorResponse handleConflict(DataIntegrityViolationException ex) {
        return new ErrorResponse("CONFLICT", "Resource already exists");
    }
    
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleUnexpected(Exception ex) {
        log.error("Unexpected error", ex);
        return new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred");
    }
}

public record ErrorResponse(
    String code,
    String message,
    @JsonInclude(JsonInclude.Include.NON_NULL)
    Map<String, String> details
) {
    public ErrorResponse(String code, String message) {
        this(code, message, null);
    }
}
```

---

## Phase 5: Security

### Spring Security 6 Configuration

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())  // Disable for stateless APIs
            .cors(cors -> cors.configurationSource(corsConfig()))
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers("/actuator/health/**").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtConverter()))
            )
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint((req, res, e) -> {
                    res.setStatus(401);
                    res.getWriter().write("{\"code\":\"UNAUTHORIZED\",\"message\":\"Invalid or missing token\"}");
                })
            )
            .headers(headers -> headers
                .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
                .frameOptions(HeadersConfigurer.FrameOptionsConfig::deny)
            )
            .build();
    }
    
    private CorsConfigurationSource corsConfig() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("https://app.example.com"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
        config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
        config.setMaxAge(3600L);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", config);
        return source;
    }
    
    private JwtAuthenticationConverter jwtConverter() {
        JwtGrantedAuthoritiesConverter authorities = new JwtGrantedAuthoritiesConverter();
        authorities.setAuthorityPrefix("ROLE_");
        authorities.setAuthoritiesClaimName("roles");
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(authorities);
        return converter;
    }
}
```

### 10-Point Security Checklist

| # | Check | Priority |
|---|-------|----------|
| 1 | CSRF disabled for stateless APIs, enabled for session-based | P0 |
| 2 | CORS configured with specific origins (no wildcards in prod) | P0 |
| 3 | JWT validation with proper issuer/audience checks | P0 |
| 4 | Input validation on all request DTOs (`@Valid`) | P0 |
| 5 | SQL injection prevention (parameterized queries only) | P0 |
| 6 | Secrets in environment variables or vault (never in code) | P0 |
| 7 | Security headers (CSP, X-Frame-Options, HSTS) | P1 |
| 8 | Rate limiting on auth endpoints | P1 |
| 9 | Dependency vulnerability scanning (OWASP, Snyk) | P1 |
| 10 | Method-level security (`@PreAuthorize`) for sensitive operations | P1 |

---

## Phase 6: Service Layer & Business Logic

### Service Pattern

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)  // Default read-only
@Slf4j
public class UserService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final ApplicationEventPublisher eventPublisher;
    
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found: " + id));
    }
    
    public Page<User> findUsers(UserStatus status, Pageable pageable) {
        if (status != null) {
            return userRepository.findByStatus(status, pageable);
        }
        return userRepository.findAll(pageable);
    }
    
    @Transactional  // Write transaction
    public User create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new ConflictException("Email already registered: " + request.email());
        }
        
        User user = User.builder()
            .email(request.email())
            .name(request.name())
            .status(UserStatus.ACTIVE)
            .build();
        
        user = userRepository.save(user);
        
        eventPublisher.publishEvent(new UserCreatedEvent(user.getId(), user.getEmail()));
        log.info("User created: id={}, email={}", user.getId(), user.getEmail());
        
        return user;
    }
    
    @Transactional
    @CacheEvict(value = "users", key = "#id")
    public User update(Long id, UpdateUserRequest request) {
        User user = findById(id);
        // Update fields...
        return userRepository.save(user);
    }
}
```

### Domain Events

```java
public record UserCreatedEvent(Long userId, String email) {}

@Component
@RequiredArgsConstructor
@Slf4j
public class UserEventListener {
    
    private final EmailService emailService;
    
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    @Async
    public void onUserCreated(UserCreatedEvent event) {
        log.info("Sending welcome email to user: {}", event.userId());
        emailService.sendWelcome(event.email());
    }
}
```

---

## Phase 7: Caching

### Redis Cache Configuration

```java
@Configuration
@EnableCaching
public class CacheConfig {
    
    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory factory) {
        RedisCacheConfiguration defaults = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofHours(1))
            .serializeValuesWith(
                RedisSerializationContext.SerializationPair.fromSerializer(
                    new GenericJackson2JsonRedisSerializer()
                ))
            .disableCachingNullValues();
        
        Map<String, RedisCacheConfiguration> configs = Map.of(
            "users", defaults.entryTtl(Duration.ofMinutes(30)),
            "products", defaults.entryTtl(Duration.ofHours(2)),
            "config", defaults.entryTtl(Duration.ofHours(24))
        );
        
        return RedisCacheManager.builder(factory)
            .cacheDefaults(defaults)
            .withInitialCacheConfigurations(configs)
            .build();
    }
}
```

### Cache Usage

```java
@Cacheable(value = "users", key = "#id")
public UserResponse getUserById(Long id) { ... }

@CachePut(value = "users", key = "#result.id")
public UserResponse updateUser(Long id, UpdateUserRequest req) { ... }

@CacheEvict(value = "users", key = "#id")
public void deleteUser(Long id) { ... }

@CacheEvict(value = "users", allEntries = true)
@Scheduled(fixedRate = 3600000)  // Hourly full invalidation
public void evictAllUsers() { ... }
```

---

## Phase 8: Resilience

### Resilience4j Configuration

```yaml
resilience4j:
  circuitbreaker:
    instances:
      payment-service:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3
        slow-call-duration-threshold: 2s
        slow-call-rate-threshold: 80
  
  retry:
    instances:
      payment-service:
        max-attempts: 3
        wait-duration: 500ms
        exponential-backoff-multiplier: 2
        retry-exceptions:
          - java.io.IOException
          - java.util.concurrent.TimeoutException
        ignore-exceptions:
          - com.example.exception.BusinessException
  
  ratelimiter:
    instances:
      api:
        limit-for-period: 100
        limit-refresh-period: 1s
        timeout-duration: 0s
```

### Usage

```java
@CircuitBreaker(name = "payment-service", fallbackMethod = "paymentFallback")
@Retry(name = "payment-service")
public PaymentResponse processPayment(PaymentRequest request) {
    return paymentClient.charge(request);
}

private PaymentResponse paymentFallback(PaymentRequest request, Throwable t) {
    log.warn("Payment service unavailable, queuing for retry: {}", t.getMessage());
    paymentQueue.enqueue(request);
    return PaymentResponse.pending();
}
```

---

## Phase 9: Observability

### Structured Logging

```java
// logback-spring.xml
// Use JSON format in production
@Slf4j
public class OrderService {
    
    public Order processOrder(CreateOrderRequest request) {
        try (var mdc = MDC.putCloseable("orderId", request.orderId());
             var userMdc = MDC.putCloseable("userId", request.userId())) {
            
            log.info("Processing order: items={}, total={}", 
                     request.items().size(), request.total());
            // All logs within this scope include orderId + userId
        }
    }
}
```

### Metrics with Micrometer

```java
@Component
@RequiredArgsConstructor
public class OrderMetrics {
    
    private final MeterRegistry registry;
    
    public void recordOrderProcessed(String status, Duration duration) {
        registry.counter("orders.processed", "status", status).increment();
        registry.timer("orders.processing.time", "status", status)
                .record(duration);
    }
    
    public void recordActiveOrders(int count) {
        registry.gauge("orders.active", count);
    }
}
```

### Health Indicators

```java
@Component
public class PaymentServiceHealthIndicator implements HealthIndicator {
    
    private final PaymentClient paymentClient;
    
    @Override
    public Health health() {
        try {
            paymentClient.ping();
            return Health.up().withDetail("latency", "ok").build();
        } catch (Exception e) {
            return Health.down().withException(e).build();
        }
    }
}
```

---

## Phase 10: Testing

### Test Pyramid

| Level | What | Tools | Coverage Target |
|-------|------|-------|----------------|
| Unit | Services, mappers, utils | JUnit 5 + Mockito | 80% |
| Slice | Controllers, repositories | @WebMvcTest, @DataJpaTest | Key paths |
| Integration | Full flow with real DB | @SpringBootTest + Testcontainers | Happy + error |
| Contract | API contracts | Spring Cloud Contract / Pact | All endpoints |

### Unit Test Pattern

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock UserRepository userRepository;
    @Mock ApplicationEventPublisher eventPublisher;
    @InjectMocks UserService userService;
    
    @Test
    void create_validRequest_savesAndPublishesEvent() {
        var request = new CreateUserRequest("test@example.com", "Test User", UserRole.USER);
        var savedUser = User.builder().id(1L).email(request.email()).build();
        
        when(userRepository.existsByEmail(request.email())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        
        User result = userService.create(request);
        
        assertThat(result.getId()).isEqualTo(1L);
        verify(eventPublisher).publishEvent(any(UserCreatedEvent.class));
    }
    
    @Test
    void create_duplicateEmail_throwsConflict() {
        var request = new CreateUserRequest("existing@example.com", "Test", UserRole.USER);
        when(userRepository.existsByEmail(request.email())).thenReturn(true);
        
        assertThatThrownBy(() -> userService.create(request))
            .isInstanceOf(ConflictException.class)
            .hasMessageContaining("already registered");
    }
}
```

### Controller Slice Test

```java
@WebMvcTest(UserController.class)
@Import(SecurityConfig.class)
class UserControllerTest {
    
    @Autowired MockMvc mockMvc;
    @MockBean UserService userService;
    @MockBean UserMapper userMapper;
    
    @Test
    @WithMockUser(roles = "USER")
    void getUser_exists_returns200() throws Exception {
        var user = User.builder().id(1L).email("test@test.com").build();
        var response = new UserResponse(1L, "test@test.com", "Test", UserStatus.ACTIVE, Instant.now());
        
        when(userService.findById(1L)).thenReturn(user);
        when(userMapper.toResponse(user)).thenReturn(response);
        
        mockMvc.perform(get("/api/v1/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.email").value("test@test.com"));
    }
}
```

### Integration Test with Testcontainers

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class UserIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Autowired TestRestTemplate restTemplate;
    
    @Test
    void fullUserLifecycle() {
        // Create
        var createReq = new CreateUserRequest("int@test.com", "Integration", UserRole.USER);
        var created = restTemplate.postForEntity("/api/v1/users", createReq, UserResponse.class);
        assertThat(created.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        
        // Read
        var fetched = restTemplate.getForEntity(
            "/api/v1/users/" + created.getBody().id(), UserResponse.class);
        assertThat(fetched.getBody().email()).isEqualTo("int@test.com");
    }
}
```

### 7 Testing Rules

1. **Constructor injection enables easy mocking** — no reflection hacks
2. **Use `@WebMvcTest` for controller tests** — loads only web layer
3. **Use `@DataJpaTest` for repository tests** — auto-configures JPA + rollback
4. **Testcontainers for integration tests** — real Postgres/Redis, not H2
5. **Test security** — `@WithMockUser`, `@WithAnonymousUser`
6. **Test validation** — ensure `@Valid` rejects bad input
7. **Don't test framework code** — test YOUR logic, not Spring's

---

## Phase 11: Performance Optimization

### Priority Stack

| # | Technique | Impact | Effort |
|---|-----------|--------|--------|
| 1 | Fix N+1 queries (JOIN FETCH / EntityGraph) | ★★★★★ | Low |
| 2 | Add database indexes on filtered/sorted columns | ★★★★★ | Low |
| 3 | Connection pool tuning (HikariCP) | ★★★★☆ | Low |
| 4 | Redis caching for read-heavy data | ★★★★☆ | Medium |
| 5 | DTO projections instead of full entities | ★★★★☆ | Medium |
| 6 | Async processing for non-critical tasks (@Async) | ★★★☆☆ | Medium |
| 7 | Virtual threads (Java 21+) for I/O-bound workloads | ★★★☆☆ | Low |
| 8 | GraalVM native compilation for cold start | ★★★☆☆ | High |

### Virtual Threads (Java 21+)

```yaml
# application.yml — enable virtual threads
spring:
  threads:
    virtual:
      enabled: true  # Tomcat uses virtual threads for requests
```

### Async Processing

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    
    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        return executor;
    }
}

@Async
public CompletableFuture<Report> generateReport(Long userId) {
    // Runs on thread pool, doesn't block request thread
    Report report = reportGenerator.generate(userId);
    return CompletableFuture.completedFuture(report);
}
```

---

## Phase 12: Deployment

### Multi-Stage Dockerfile

```dockerfile
# Build
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app
COPY gradle/ gradle/
COPY gradlew build.gradle.kts settings.gradle.kts ./
RUN ./gradlew dependencies --no-daemon  # Cache deps
COPY src/ src/
RUN ./gradlew bootJar --no-daemon -x test

# Runtime
FROM eclipse-temurin:21-jre-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
USER app
EXPOSE 8080

# JVM tuning for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
  -XX:MaxRAMPercentage=75.0 \
  -XX:InitialRAMPercentage=50.0 \
  -XX:+UseG1GC \
  -XX:+ExitOnOutOfMemoryError \
  -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### GitHub Actions CI/CD

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 21
          cache: gradle
      
      - name: Build & Test
        run: ./gradlew build
        env:
          DATABASE_URL: jdbc:postgresql://localhost:5432/testdb
          DATABASE_USERNAME: test
          DATABASE_PASSWORD: test
      
      - name: Build Docker Image
        if: github.ref == 'refs/heads/main'
        run: |
          docker build -t ${{ secrets.REGISTRY }}/app:${{ github.sha }} .
          docker push ${{ secrets.REGISTRY }}/app:${{ github.sha }}
```

### Production Readiness Checklist

**P0 — Mandatory:**
- [ ] `open-in-view: false`
- [ ] `ddl-auto: validate` + Flyway/Liquibase migrations
- [ ] HikariCP pool configured with leak detection
- [ ] Graceful shutdown enabled
- [ ] Health + readiness endpoints exposed
- [ ] Global exception handler (no stack traces in responses)
- [ ] Input validation on all request DTOs
- [ ] Security configured (auth, CORS, headers)
- [ ] Structured JSON logging
- [ ] Prometheus metrics exported

**P1 — Within 30 days:**
- [ ] Circuit breakers on external calls
- [ ] Redis caching for hot paths
- [ ] Virtual threads enabled (Java 21+)
- [ ] Container resource limits set
- [ ] Dependency vulnerability scanning in CI

---

## Phase 13: Kotlin-Specific Patterns

If using Kotlin instead of Java:

```kotlin
// Coroutines + WebFlux
@RestController
@RequestMapping("/api/v1/users")
class UserController(private val userService: UserService) {
    
    @GetMapping("/{id}")
    suspend fun getUser(@PathVariable id: Long): UserResponse =
        userService.findById(id).toResponse()
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    suspend fun createUser(@Valid @RequestBody request: CreateUserRequest): UserResponse =
        userService.create(request).toResponse()
}

// Data classes as DTOs (no Lombok needed)
data class CreateUserRequest(
    @field:NotBlank @field:Email
    val email: String,
    @field:NotBlank @field:Size(min = 2, max = 100)
    val name: String,
)

// Extension functions for mapping
fun User.toResponse() = UserResponse(
    id = id,
    email = email,
    name = name,
    status = status,
    createdAt = createdAt,
)
```

**Kotlin advantages**: null safety, data classes (no Lombok), coroutines for async, extension functions for mapping, sealed classes for error hierarchies.

---

## Phase 14: Advanced Patterns

### Scheduled Jobs

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class CleanupJob {
    
    private final UserRepository userRepository;
    
    @Scheduled(cron = "0 0 2 * * *")  // 2 AM daily
    @SchedulerLock(name = "cleanup", lockAtMostFor = "30m")  // ShedLock for distributed
    public void cleanupInactiveUsers() {
        int count = userRepository.deactivateInactiveUsers(
            UserStatus.INACTIVE,
            Instant.now().minus(90, ChronoUnit.DAYS)
        );
        log.info("Deactivated {} inactive users", count);
    }
}
```

### Kafka Integration

```java
@Component
@RequiredArgsConstructor
public class OrderEventProducer {
    
    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;
    
    public void publishOrderCreated(Order order) {
        var event = new OrderEvent("ORDER_CREATED", order.getId(), Instant.now());
        kafkaTemplate.send("orders", order.getId().toString(), event);
    }
}

@Component
@KafkaListener(topics = "orders", groupId = "notification-service")
public class OrderEventConsumer {
    
    @KafkaHandler
    public void handleOrderEvent(OrderEvent event) {
        // Process event with idempotency check
    }
}
```

### Multi-Tenancy

```java
@Component
public class TenantFilter extends OncePerRequestFilter {
    
    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                     HttpServletResponse response,
                                     FilterChain chain) throws ServletException, IOException {
        String tenantId = request.getHeader("X-Tenant-ID");
        if (tenantId != null) {
            TenantContext.setTenantId(tenantId);
        }
        try {
            chain.doFilter(request, response);
        } finally {
            TenantContext.clear();
        }
    }
}
```

---

## 10 Common Mistakes

| # | Mistake | Fix |
|---|---------|-----|
| 1 | `open-in-view: true` (default!) | Set `false` — prevents lazy loading outside transaction |
| 2 | `ddl-auto: update` in production | Use Flyway/Liquibase — predictable, reversible migrations |
| 3 | Field injection (`@Autowired`) | Constructor injection — testable, explicit dependencies |
| 4 | Returning JPA entities from controllers | Use DTOs — prevents lazy loading errors + data leaks |
| 5 | Not configuring HikariCP | Tune pool size, timeouts, leak detection |
| 6 | Catching `Exception` everywhere | Specific exceptions + global handler |
| 7 | No pagination on list endpoints | Always paginate — `Pageable` parameter |
| 8 | Blocking calls in reactive stack | Don't mix blocking JPA with WebFlux |
| 9 | Missing `@Transactional(readOnly=true)` | Optimizes read queries (no dirty checking) |
| 10 | Testing with H2 instead of real DB | Testcontainers — H2 hides real SQL issues |

---

## Quality Rubric (0-100)

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Architecture | 15% | Clean layers, DI, no circular deps |
| Data Access | 15% | N+1 free, indexed, migrations managed |
| Security | 15% | Auth, validation, headers, secrets management |
| Testing | 15% | Pyramid coverage, Testcontainers, slice tests |
| API Design | 10% | Consistent errors, pagination, OpenAPI docs |
| Observability | 10% | Structured logs, metrics, health checks |
| Resilience | 10% | Circuit breakers, retries, graceful shutdown |
| Deployment | 10% | Containerized, CI/CD, zero-downtime |

---

## 10 Commandments of Spring Boot Production

1. **Disable `open-in-view`** — first thing, every project
2. **Constructor injection, always** — `@RequiredArgsConstructor`
3. **DTOs at every boundary** — controllers never touch entities
4. **`@Transactional(readOnly=true)` by default** — opt-in to writes
5. **Testcontainers over H2** — test against real databases
6. **Flyway for migrations** — never `ddl-auto: update`
7. **Validate all input** — `@Valid` on every `@RequestBody`
8. **Structure your logs** — JSON in production, MDC for context
9. **Tune HikariCP** — pool size = (core_count * 2) + spindle_count
10. **Enable graceful shutdown** — `server.shutdown: graceful`

---

## Natural Language Commands

When working with Spring Boot projects, you can ask:

1. `review my Spring Boot app` → Full architecture + config audit
2. `check my JPA entities` → N+1, indexing, mapping review
3. `review my security config` → Auth, CORS, headers, vulnerabilities
4. `optimize my queries` → N+1 detection, projection opportunities
5. `set up Testcontainers` → Integration test configuration
6. `add caching` → Redis setup + cache strategy
7. `add circuit breaker` → Resilience4j configuration
8. `Dockerize my app` → Multi-stage Dockerfile + CI/CD
9. `add observability` → Actuator + Prometheus + structured logging
10. `review my tests` → Coverage gaps, missing slice tests
11. `migrate to Java 21` → Virtual threads, pattern matching, records
12. `convert to Kotlin` → Coroutines, data classes, extension functions

---

## ⚡ Level Up Your Spring Boot Skills

This free skill covers production engineering methodology. For **industry-specific AI agent context** that accelerates your Spring Boot projects:

- **[SaaS Context Pack ($47)](https://afrexai-cto.github.io/context-packs/)** — SaaS billing, multi-tenancy, subscription management patterns
- **[Fintech Context Pack ($47)](https://afrexai-cto.github.io/context-packs/)** — Payment processing, compliance, financial data patterns
- **[Healthcare Context Pack ($47)](https://afrexai-cto.github.io/context-packs/)** — HIPAA compliance, HL7/FHIR, audit logging patterns

## 🔗 More Free Skills by AfrexAI

- `afrexai-python-production` — Python production engineering
- `afrexai-api-architecture` — API design & architecture
- `afrexai-database-engineering` — Database optimization & scaling
- `afrexai-test-automation-engineering` — Test strategy & automation
- `afrexai-cicd-engineering` — CI/CD pipeline engineering

Browse all: [AfrexAI on ClawHub](https://clawhub.com) | [Context Packs Storefront](https://afrexai-cto.github.io/context-packs/)
