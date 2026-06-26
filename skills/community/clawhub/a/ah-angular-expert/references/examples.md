# Angular Expert — Code Examples

## Example 1

```typescript
// Standalone component with signals
import { Component, signal, computed, effect, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { toSignal, toObservable } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  template: `
    <div class="profile-container">
      <h2>{{ fullName() }}</h2>
      <input [(ngModel)]="firstName" (ngModelChange)="updateFirstName($event)" />
      <input [(ngModel)]="lastName" (ngModelChange)="updateLastName($event)" />
      
      <div *ngIf="loading()">Loading...</div>
      <div *ngFor="let item of filteredItems()">
        {{ item.name }} - {{ item.price | currency }}
      </div>
      
      <button (click)="increment()">Count: {{ count() }}</button>
    </div>
  `,
  styles: [`
    .profile-container {
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 8px;
    }
  `]
})
export class UserProfileComponent {
  // Signals
  firstName = signal('John');
  lastName = signal('Doe');
  count = signal(0);
  loading = signal(false);
  items = signal<Item[]>([]);
  filterText = signal('');

  // Computed signals
  fullName = computed(() => `${this.firstName()} ${this.lastName()}`);
  
  filteredItems = computed(() => {
    const filter = this.filterText().toLowerCase();
    return this.items().filter(item => 
      item.name.toLowerCase().includes(filter)
    );
  });

  // Effects
  logEffect = effect(() => {
    console.log(`Full name changed to: ${this.fullName()}`);
  });

  // Convert observable to signal
  private userService = inject(UserService);
  currentUser = toSignal(this.userService.currentUser$, { initialValue: null });

  // Convert signal to observable
  count$ = toObservable(this.count);

  constructor() {
    // Setup effect
    effect(() => {
      if (this.count() > 10) {
        console.log('Count exceeded 10!');
      }
    });
  }

  updateFirstName(value: string) {
    this.firstName.set(value);
  }

  updateLastName(value: string) {
    this.lastName.set(value);
  }

  increment() {
    this.count.update(c => c + 1);
  }

  async loadItems() {
    this.loading.set(true);
    try {
      const data = await this.fetchItems();
      this.items.set(data);
    } finally {
      this.loading.set(false);
    }
  }
}
```

## Example 2

```typescript
import { Injectable } from '@angular/core';
import {
  Observable, Subject, BehaviorSubject, ReplaySubject,
  combineLatest, merge, concat, forkJoin, race,
  from, of, interval, timer, EMPTY, throwError
} from 'rxjs';
import {
  map, filter, tap, switchMap, mergeMap, concatMap, exhaustMap,
  debounceTime, throttleTime, distinctUntilChanged,
  retry, retryWhen, catchError, finalize,
  take, takeUntil, takeWhile, skip, skipUntil,
  scan, reduce, shareReplay, share,
  withLatestFrom, startWith, delay
} from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class DataService {
  private destroy$ = new Subject<void>();
  private cache$ = new BehaviorSubject<Map<string, any>>(new Map());

  // Advanced search with debounce and cancellation
  search(query$: Observable<string>): Observable<SearchResult[]> {
    return query$.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      filter(query => query.length >= 3),
      switchMap(query => 
        this.http.get<SearchResult[]>(`/api/search?q=${query}`).pipe(
          retry(3),
          catchError(error => {
            console.error('Search failed:', error);
            return of([]);
          })
        )
      ),
      shareReplay(1)
    );
  }

  // Polling with exponential backoff
  pollData(): Observable<Data> {
    return interval(5000).pipe(
      startWith(0),
      switchMap(() => this.fetchData()),
      retryWhen(errors =>
        errors.pipe(
          scan((retryCount, error) => {
            if (retryCount >= 3) {
              throw error;
            }
            return retryCount + 1;
          }, 0),
          delay(retryCount => Math.pow(2, retryCount) * 1000)
        )
      ),
      takeUntil(this.destroy$)
    );
  }

  // Combine multiple streams
  getDashboardData(): Observable<DashboardData> {
    return combineLatest([
      this.getUserStats(),
      this.getRecentActivity(),
      this.getNotifications()
    ]).pipe(
      map(([stats, activity, notifications]) => ({
        stats,
        activity,
        notifications
      })),
      catchError(error => {
        console.error('Dashboard data failed:', error);
        return of(this.getDefaultDashboardData());
      })
    );
  }

  // Caching with refresh
  getCachedData(key: string, fetch: () => Observable<any>): Observable<any> {
    const cached = this.cache$.value.get(key);
    
    if (cached && !this.isExpired(cached)) {
      return of(cached.data);
    }

    return fetch().pipe(
      tap(data => {
        const newCache = new Map(this.cache$.value);
        newCache.set(key, { data, timestamp: Date.now() });
        this.cache$.next(newCache);
      }),
      shareReplay(1)
    );
  }

  // Race conditions handling
  getFirstAvailable(): Observable<any> {
    return race([
      this.primarySource().pipe(
        timeout(3000),
        catchError(() => EMPTY)
      ),
      this.fallbackSource().pipe(delay(1000))
    ]);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Example 3

```typescript
// Custom injection token
import { InjectionToken, inject } from '@angular/core';

export interface AppConfig {
  apiUrl: string;
  version: string;
  features: string[];
}

export const APP_CONFIG = new InjectionToken<AppConfig>('app.config');

// Provider configuration
export const appConfig: AppConfig = {
  apiUrl: environment.apiUrl,
  version: '1.0.0',
  features: ['feature1', 'feature2']
};

// In main.ts for standalone
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(
      withInterceptors([authInterceptor, errorInterceptor])
    ),
    provideAnimations(),
    { provide: APP_CONFIG, useValue: appConfig },
    {
      provide: LoggerService,
      useFactory: (config: AppConfig) => {
        return new LoggerService(config.version);
      },
      deps: [APP_CONFIG]
    }
  ]
});

// Using injection
@Component({
  selector: 'app-feature',
  standalone: true,
  template: ``
})
export class FeatureComponent {
  private config = inject(APP_CONFIG);
  private logger = inject(LoggerService);
  
  constructor() {
    this.logger.log(`API URL: ${this.config.apiUrl}`);
  }
}
```

## Example 4

```typescript
import { Component } from '@angular/core';
import {
  FormBuilder, FormGroup, FormArray, FormControl,
  Validators, AbstractControl, ValidationErrors,
  AsyncValidatorFn
} from '@angular/forms';

// Custom validators
export class CustomValidators {
  static email(control: AbstractControl): ValidationErrors | null {
    const email = control.value;
    if (!email) return null;
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email) ? null : { email: true };
  }

  static matchPasswords(passwordKey: string, confirmKey: string) {
    return (group: AbstractControl): ValidationErrors | null => {
      const password = group.get(passwordKey);
      const confirm = group.get(confirmKey);
      
      if (!password || !confirm) return null;
      
      return password.value === confirm.value ? null : { mismatch: true };
    };
  }

  static uniqueEmail(userService: UserService): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      if (!control.value) {
        return of(null);
      }

      return timer(300).pipe(
        switchMap(() => userService.checkEmail(control.value)),
        map(exists => exists ? { emailTaken: true } : null),
        catchError(() => of(null))
      );
    };
  }
}

@Component({
  selector: 'app-dynamic-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <div formGroupName="personal">
        <input formControlName="name" placeholder="Name" />
        <div *ngIf="name?.invalid && name?.touched">
          <span *ngIf="name?.errors?.['required']">Name is required</span>
        </div>
        
        <input formControlName="email" placeholder="Email" />
        <div *ngIf="email?.pending">Checking email...</div>
        <div *ngIf="email?.invalid && email?.touched">
          <span *ngIf="email?.errors?.['emailTaken']">Email already taken</span>
        </div>
      </div>

      <div formArrayName="skills">
        <div *ngFor="let skill of skills.controls; let i = index">
          <input [formControlName]="i" placeholder="Skill" />
          <button type="button" (click)="removeSkill(i)">Remove</button>
        </div>
        <button type="button" (click)="addSkill()">Add Skill</button>
      </div>

      <button type="submit" [disabled]="form.invalid">Submit</button>
    </form>
  `
})
export class DynamicFormComponent {
  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private userService: UserService
  ) {
    this.form = this.fb.group({
      personal: this.fb.group({
        name: ['', [Validators.required, Validators.minLength(3)]],
        email: ['', 
          [Validators.required, CustomValidators.email],
          [CustomValidators.uniqueEmail(this.userService)]
        ]
      }),
      skills: this.fb.array([
        this.createSkillControl()
      ])
    });

    // Dynamic form updates
    this.form.get('personal.name')?.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(value => {
      console.log('Name changed:', value);
    });
  }

  get name() { return this.form.get('personal.name'); }
  get email() { return this.form.get('personal.email'); }
  get skills() { return this.form.get('skills') as FormArray; }

  createSkillControl(): FormControl {
    return this.fb.control('', Validators.required);
  }

  addSkill() {
    this.skills.push(this.createSkillControl());
  }

  removeSkill(index: number) {
    this.skills.removeAt(index);
  }

  onSubmit() {
    if (this.form.valid) {
      console.log('Form data:', this.form.value);
    }
  }
}
```

## Example 5

```typescript
// Functional guards (Angular 14+)
import { inject } from '@angular/core';
import { Router, CanActivateFn, CanDeactivateFn } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree(['/login'], {
    queryParams: { returnUrl: state.url }
  });
};

export const roleGuard: CanActivateFn = (route) => {
  const authService = inject(AuthService);
  const requiredRole = route.data['role'];

  return authService.hasRole(requiredRole);
};

export const canDeactivateGuard: CanDeactivateFn<CanComponentDeactivate> = 
  (component) => {
    return component.canDeactivate ? component.canDeactivate() : true;
  };

// HTTP Interceptor
import { HttpInterceptorFn, HttpRequest, HttpHandlerFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (
  req: HttpRequest<any>,
  next: HttpHandlerFn
) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  return next(req);
};

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const toastr = inject(ToastrService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        router.navigate(['/login']);
      } else if (error.status === 403) {
        toastr.error('Access denied');
      } else if (error.status >= 500) {
        toastr.error('Server error occurred');
      }

      return throwError(() => error);
    })
  );
};
```

## Example 6

```typescript
// Component testing
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

describe('UserProfileComponent', () => {
  let component: UserProfileComponent;
  let fixture: ComponentFixture<UserProfileComponent>;
  let userService: jasmine.SpyObj<UserService>;

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('UserService', ['getUser', 'updateUser']);

    await TestBed.configureTestingModule({
      imports: [UserProfileComponent],
      providers: [
        { provide: UserService, useValue: spy }
      ]
    }).compileComponents();

    userService = TestBed.inject(UserService) as jasmine.SpyObj<UserService>;
    fixture = TestBed.createComponent(UserProfileComponent);
    component = fixture.componentInstance;
  });

  it('should display user name', () => {
    component.firstName.set('John');
    component.lastName.set('Doe');
    fixture.detectChanges();

    const nameElement = fixture.debugElement.query(By.css('h2'));
    expect(nameElement.nativeElement.textContent).toContain('John Doe');
  });

  it('should increment count on button click', () => {
    const button = fixture.debugElement.query(By.css('button'));
    
    button.nativeElement.click();
    fixture.detectChanges();

    expect(component.count()).toBe(1);
  });
});

// Service testing with HttpClient
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('DataService', () => {
  let service: DataService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [DataService]
    });

    service = TestBed.inject(DataService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should fetch data', () => {
    const mockData = { id: 1, name: 'Test' };

    service.getData().subscribe(data => {
      expect(data).toEqual(mockData);
    });

    const req = httpMock.expectOne('/api/data');
    expect(req.request.method).toBe('GET');
    req.flush(mockData);
  });
});
```
