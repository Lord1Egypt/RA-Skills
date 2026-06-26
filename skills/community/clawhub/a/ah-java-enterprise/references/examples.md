# Java Enterprise — Code Examples

## Example 1

```java
// Spring Boot configuration
@SpringBootApplication
@EnableCaching
@EnableAsync
@EnableScheduling
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// REST Controller with validation
@RestController
@RequestMapping("/api/v1/users")
@Validated
@Slf4j
public class UserController {
    
    private final UserService userService;
    
    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(
            @PathVariable @UUID String id,
            @RequestHeader("X-Request-ID") String requestId) {
        
        log.info("Fetching user: {} with requestId: {}", id, requestId);
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDto createUser(@Valid @RequestBody CreateUserRequest request) {
        return userService.create(request);
    }
    
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidation(ValidationException e) {
        return ResponseEntity.badRequest()
            .body(new ErrorResponse(e.getMessage(), e.getErrors()));
    }
}
```

## Example 2

```java
// JVM options for production
/*
-Xms2g -Xmx2g
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/log/app/
-Dspring.profiles.active=production
-Djava.security.egd=file:/dev/./urandom
*/

// Performance monitoring
@Component
@Slf4j
public class PerformanceMonitor {
    
    private final MeterRegistry meterRegistry;
    
    @EventListener
    public void handleContextRefresh(ContextRefreshedEvent event) {
        Runtime runtime = Runtime.getRuntime();
        
        Gauge.builder("jvm.memory.used", runtime, Runtime::totalMemory)
            .baseUnit("bytes")
            .register(meterRegistry);
        
        Gauge.builder("jvm.memory.max", runtime, Runtime::maxMemory)
            .baseUnit("bytes")
            .register(meterRegistry);
    }
    
    @Aspect
    @Component
    public static class PerformanceAspect {
        
        @Around("@annotation(Monitored)")
        public Object monitor(ProceedingJoinPoint joinPoint) throws Throwable {
            long start = System.currentTimeMillis();
            
            try {
                return joinPoint.proceed();
            } finally {
                long duration = System.currentTimeMillis() - start;
                log.info("Method {} took {} ms", 
                    joinPoint.getSignature().toShortString(), duration);
            }
        }
    }
}
```
